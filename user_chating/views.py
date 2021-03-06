from uuid import uuid4
from django.db import close_old_connections
import threading
from datetime import timedelta
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import Context
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
import email
from .models import Users, UsersAuth, is_authorized, Chats, Messages, DeletedMessages, ChatsWithOverLimits
import json
import random
from django.views.decorators.csrf import csrf_exempt
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
import rsa
import secrets
from base64 import b64decode
import urllib.parse
import hashlib

# Create your views here.
def index(request):
    if 'token' in request.COOKIES:
        if is_authorized(request.COOKIES['token']):
            return redirect('/lk')
    if request.method == 'POST':
        if request.POST['token'] == '1':
            username = request.POST['username']
            password = hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest()
            print(password)
            user = Users.objects.filter(username=username, password=password)
            if user:
                token = uuid4()
                usr = UsersAuth(username=username, token=token)
                usr.save()
                response = redirect('/lk')
                if 'check' in request.POST:
                    response.set_cookie(key='token', value=token, max_age=5184000)
                else:
                    response.set_cookie(key='token', value=token)
                return response
            return render(request, 'regform.html', {'msg': ["Неверное имя пользователя или пароль!"]})
        else:
            username = request.POST['username']
            password = hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest()
            #firstname = request.POST['firstname']
            #secondname = request.POST['secondname']
            email = request.POST['email']
            if Users.objects.filter(username=username).exists():
                return render(request, 'regform.html', {'msg': ['Такой пользователь уже существует. Пожалуйста, авторизируйтесь!']})
            user = Users(username=username, email=email, password=password)
            user.save()
            if user:
                token = uuid4()
                usr = UsersAuth(username=username, token=token)
                usr.save()
                #token = usr.login(username=username)
                response = redirect('/lk')
                if 'check' in request.POST:
                    response.set_cookie(key='token', value=token, max_age=5184000)
                else:
                    response.set_cookie(key='token', value=token)
                return response
    else:
        return render(request, 'regform.html', context={})


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not ('token' in request.COOKIES):
            return redirect('/')
        if not is_authorized(request.COOKIES['token']):
            return redirect('/')
        res = func(request, *args, **kwargs)
        return res
    return wrapper


@login_required
def lk(request):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    chats = Chats.objects.filter(users=user).order_by('id')
    render_chats_arr = []
    for index, chat in enumerate(chats):
        render_chat = {}
        render_chat["index"] = "files/images/"+str(index+1)+".jpg"
        render_chat["name"] = chat.title
        render_chat["url"] = chat.url
        render_chats_arr.append(render_chat)

    response = render(request, 'lk.html', context={"username": "USERNAME!!!", "chats": render_chats_arr})
    print(request.COOKIES['token'])
    return response


@login_required
def logout(request):
    UsersAuth.objects.filter(token=request.COOKIES['token']).delete()
    return redirect('/')


@login_required
def create_chat(request):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    if request.method == 'POST':
        title = request.POST['title']
        chat = Chats(title=title, url=uuid4())
        chat.save()
        chat.users.add(user)
        chat.save()
        return redirect('../')
    return render(request, 'create_chat.html', context={})


@login_required
def delete_chat(request):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    if request.method == 'POST':
        check_values = request.POST.getlist('chat[]')
        for chat in check_values:
            rem_chat = Chats.objects.filter(url=chat).first()
            rem_chat.users.remove(user)
            rem_chat.save()
        return redirect('../')

    chats = Chats.objects.filter(users=user)
    if not chats:
        return redirect('../')
    return render(request, 'del_chat.html', context={"chats": chats})


@csrf_exempt
@login_required
def chatting(request, url):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    chat = Chats.objects.filter(users=user, url=url).first()
    if request.method == 'POST':
        new_msg = Messages(username=user.username, message=request.POST['msg'], senddate=datetime.datetime.utcnow())
        new_msg.save()
        new_msg.chats.add(chat)
        new_msg.save()
        return HttpResponse('true')

    if not chat:
        return redirect('../')
    messages = Messages.objects.filter(chats=chat).order_by('id')
    CWOL = ChatsWithOverLimits.objects.filter(chat_url=chat.url).first()
    #msg_user_havent_seen_yet = Messages.objects.filter(chats=chat, senddate__gt=user.when_online).first()
    msg_user_havent_seen_yet = Messages.objects.filter(chats=chat).exclude(
                                                    users_read_message__username=user.username).first()
    limits_are_over = False
    if CWOL:
        limits_are_over = True
    #print(messages)
    me = user.username
    users = []
    users_in_chat = chat.users.all()
    for u in users_in_chat:
        users.append(u.username)

    return render(request, 'chatting.html', context={"chat": chat, "messages": messages, "users": users, "me": me,
                                                     "limits_are_over": limits_are_over,
                                                     'msg_user_havent_seen_yet':msg_user_havent_seen_yet})


@login_required
def get_message(request):
    if 'val' in request.headers and 'url' in request.headers:
        val = request.headers['val']
        url = request.headers['url']

    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    chat = Chats.objects.filter(users=user, url=url).first()
    new_message = Messages.objects.filter(id__gt=int(val), chats=chat).first()
    if new_message:
        g_username = new_message.username
        g_me = user.username
        g_message = new_message.message
        g_send_date = new_message.senddate
        response = HttpResponse(json.dumps({"key": "value", "msg_val": new_message.id,
                                            "username": g_username, "me": g_me,
                                            "message":g_message, "senddate":  str(datetime.datetime.strftime(g_send_date, "%d.%m %H:%M"))}))
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = HttpResponse()
        response.status_code = 304
        response['Access-Control-Allow-Origin'] = '*'
        return response


@login_required
def add_users(request, url):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    chat = Chats.objects.filter(users=user, url=url).first()
    if not chat:
        return redirect('../')
    if request.method == 'POST':
        us = "user"
        user_list = []
        new_users_list = []
        for i in range(15):
            user_list.append(us+str(i+1))
        for user_l in user_list:
            if user_l in request.POST:
                new_users_list.append(user_l)

        for usr in new_users_list:
            db_user = Users.objects.filter(username=request.POST[usr]).first()
            if db_user:
                chat.users.add(db_user)
        chat.save()
        return redirect('../lk/'+url)
    if chat.is_opened:
        status = 1
    else:
        status = 3
    print(status)
    return render(request, 'add_users.html', context={"url": url, "status": status})


@login_required
def check_online(request, url):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    user.is_online = True
    user.when_online = datetime.datetime.utcnow()
    user.next_status_send = datetime.datetime.utcnow()+datetime.timedelta(seconds=60)
    user.save()
    chat = Chats.objects.filter(users=user, url=url).first()
    last_msg = Messages.objects.filter(chats=chat).exclude(users_read_message__username=user.username)
    for message in last_msg:
        message.users_read_message.add(user)
        message.save()
    users_in_chat = chat.users.order_by('username').all()
    users = []
    for u in users_in_chat:
        users.append({"username": u.username, "is_online": u.is_online})
    return HttpResponse(json.dumps(users))


@login_required
def edit_userinfo(request):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    if request.method == 'POST':
        username = request.POST['username']
        password = hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest()
        firstname = request.POST['firstname']
        secondname = request.POST['secondname']
        email = request.POST['email']
        if username == "" or password == "":
            return render(request, 'edit_userinfo.html', context={"user": user})
        if not (user.username == username):
            us_exist = Users.objects.filter(username=username).first()
            if not us_exist:
                Users.objects.filter(username=user.username).delete()
                new_user = Users(username=username, password=password, firstname=firstname,
                                 secondname=secondname, email=email)
                new_user.save()
                auth.username = new_user.username
                auth.save()
                return render(request, 'edit_userinfo.html', context={"user": new_user})
        user.password = password
        user.firstname = firstname
        user.secondname = secondname
        user.email = email
        user.save()
        #return redirect('../')
    return render(request, 'edit_userinfo.html', context={"user": user})


@login_required
def open_access_to_chat(request, url):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    chat = Chats.objects.filter(users=user, url=url).first()
    if not chat:
        return HttpResponse('not ok')
    if request.headers['open'] == '0':
        chat.is_opened = False
        chat.save()
        return HttpResponse('Chat closed')
    else:
        chat.is_opened = True
        chat.save()
        return HttpResponse('Chat opened')


def get_access_to_chat(request, url):

    if request.method == 'POST':
        if request.POST['token'] == '1':
            username = request.POST['username']
            password = hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest()
            user = Users.objects.filter(username=username, password=password)
            if user:
                print("Нашел юзера!")
                token = uuid4()
                usr = UsersAuth(username=username, token=token)
                usr.save()

                user = Users.objects.filter(username=usr.username).first()
                chat = Chats.objects.filter(url=url).first()
                if not chat:
                    return render(request, 'get_access_to_chat.html', context={'msg': "Такого чата не существует!",
                                                                               'status': 1})
                if not chat.is_opened:
                    return render(request, 'get_access_to_chat.html',
                                  context={'msg': "Доступ к чату закрыт. Попросите владельца "
                                                  "чата открыть доступ или добавить Вас вручную.",
                                           'status': 2})
                chat.users.add(user)
                chat.save()

                response = render(request, 'get_access_to_chat.html',
                                  context={'msg': "Вы были успешно добавлены в чат . \n"
                                                  "Теперь Вы можете перейти на главную страницу.",
                                           'status': 3})
                print(token)
                if 'check' in request.POST:
                    response.set_cookie(key='token', value=token, max_age=5184000)
                else:
                    response.set_cookie(key='token', value=token)
                return response
            return render(request, 'get_access_to_chat.html', {'msg': ["Неверное имя пользователя или пароль!"]})
        else:
            username = request.POST['username']
            password = hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest()
            #firstname = request.POST['firstname']
            #secondname = request.POST['secondname']
            email = request.POST['email']
            if Users.objects.filter(username=username).exists():
                return render(request, 'get_access_to_chat.html', {'msg': ['Такой пользователь уже существует. Пожалуйста, авторизируйтесь!']})
            user = Users(username=username, email=email, password=password)
            user.save()
            if user:
                token = uuid4()
                usr = UsersAuth(username=username, token=token)
                usr.save()
                user = Users.objects.filter(username=usr.username).first()
                chat = Chats.objects.filter(url=url).first()
                if not chat:
                    return render(request, 'get_access_to_chat.html', context={'msg': "Такого чата не существует!",
                                                                               'status': 1})
                if not chat.is_opened:
                    return render(request, 'get_access_to_chat.html',
                                  context={'msg': "Доступ к чату закрыт. Попросите владельца "
                                                  "чата открыть доступ или добавить Вас вручную.",
                                           'status': 2})
                chat.users.add(user)
                chat.save()
                #token = usr.login(username=username)
                response = render(request, 'get_access_to_chat.html',
                                  context={'msg': "Вы были успешно добавлены в чат . \n"
                                                  "Теперь Вы можете перейти на главную страницу.",
                                           'status': 3})
                print(token)
                if 'check' in request.POST:
                    response.set_cookie(key='token', value=token, max_age=5184000)
                else:
                    response.set_cookie(key='token', value=token)
                return response

    # ------------------------////---------------------------------------------------



    auth = None
    if 'token' in request.COOKIES:
        auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    if not auth:
        return render(request, 'get_access_to_chat.html', context={'msg': "Вам необходимо зарегистрироваться "
                                                                          "либо авторизироваться!",
                                                                   'status': 0})

    user = Users.objects.filter(username=auth.username).first()
    chat = Chats.objects.filter(url=url).first()
    if not chat:
        return render(request, 'get_access_to_chat.html', context={'msg': "Такого чата не существует!",
                                                                   'status': 1})
    if not chat.is_opened:
        return render(request, 'get_access_to_chat.html', context={'msg': "Доступ к чату закрыт. Попросите владельца "
                                                                          "чата открыть доступ или добавить Вас вручную.",
                                                                   'status': 2})
    chat.users.add(user)
    chat.save()
    return render(request, 'get_access_to_chat.html', context={'msg': "Вы были успешно добавлены в чат "+chat.title+". "
                                                                      "Теперь Вы можете перейти на главную страницу.",
                                                               'status': 3})


@csrf_exempt
@login_required
def delete_message(request):
    if request.method == 'POST':
        if 'messageIdentifier' in request.headers:
            msg = Messages.objects.filter(id=int(request.headers['messageIdentifier'])).first()
            if msg:
                deleted_msg = DeletedMessages(id=msg.id, username=msg.username, message=msg.message, senddate=msg.senddate)
                deleted_msg.save()
                chats = msg.chats.all()
                for chat in chats:
                    deleted_msg.chats.add(chat)
                deleted_msg.save()
            Messages.objects.filter(id=int(request.headers['messageIdentifier'])).delete()
            return HttpResponse(True)
    return HttpResponse(True)


@csrf_exempt
@login_required
def get_delete_message(request):
    if request.method == 'POST':
        auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
        chats = Chats.objects.filter(url=request.headers['url']).first()
        deleted_msg = DeletedMessages.objects.filter(chats=chats)
        data = []
        for msg in deleted_msg:
            identifier = {}
            identifier['id'] = msg.id
            identifier['username'] = msg.username
            identifier['me'] = auth.username
            data.append(identifier)
        return HttpResponse(json.dumps(data))


def help(request):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    if request.method == 'POST':
        email = request.POST['email']
        message = request.POST['message']
        username = None
        if auth:
            username = auth.username
        send_email([settings.EMAIL_HOST_USER, ], email, str(username)+" Сообщение: "+str(message))
        return redirect("../")
    if not auth:
        return render(request, 'help.html')
    user = Users.objects.filter(username=auth.username).first()
    if not user:
        return render(request, 'help.html')
    return render(request, 'help.html', context={'username': user.username, 'email': user.email})
#
#
#ГОТОВАЯ ФУНКЦИЯ ДЛЯ ОТПРАВКИ СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЯМ, КОТОРЫЕ НЕ ОНЛАЙН
#
#
@csrf_exempt
@login_required
def send_vk_message(request):
    if request.method == 'POST':
        jsObject = request.POST
        data = []
        for J in jsObject:
            j = json.loads(J)
            if not (j is None):
                for elem in j:
                    identifier = {}
                    chats = Chats.objects.filter(url=request.headers['url']).first()
                    deleted_msg = DeletedMessages.objects.filter(chats=chats).first()
                    if deleted_msg:
                        print(deleted_msg)
                    #print(elem['username'], elem['is_online'])

        # Доделать обработку удаления сообщения!!!! Выдавать на клиент id удаленного сообщения
        return HttpResponse(json.dumps(""))


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        user = Users.objects.filter(username=username, email=email).first()
        if not user:
            return render(request, 'forgot_password.html', context={'status': 2})
        new_pasw = random.randint(10000, 99999)
        new_list_email = []
        new_list_email.append(email)
        user.password = hashlib.md5(str(new_pasw).encode('utf-8')).hexdigest()
        msg_before = "Ваш новый пароль от Link - "
        msg_after = ". Пожалуйста, авторизируйутесь и смените пароль в личном кабинете в " \
                    "разделе 'Редактировать профиль'"
        send_email(new_list_email, "Link. Password recovery", msg_before+str(new_pasw)+msg_after)
        user.save()
        return render(request, 'forgot_password.html', context={'status': 1})
    return render(request, 'forgot_password.html', context={'status': 0})
    pass


def send_email(to, header, mail):
    send_mail(subject=str(header), message=str(mail), from_email=settings.EMAIL_HOST_USER, recipient_list=to)
    return True


@csrf_exempt
def check_new_messages(request):
    result = "Новые непрочитанные сообщения в чатах: "
    result_ids = "="
    check = False
    login = request.GET['login']
    code = request.GET['code']
    user = Users.objects.filter(username=login, code=code).first()
    if not user:
        http = HttpResponse('')
        http.status_code = 401
        return http
    chats = Chats.objects.filter(users=user)
    for chat in chats:
        msg_user_havent_seen_yet = Messages.objects.filter(chats=chat).exclude(users_read_message__username=user.username).last()
        print(msg_user_havent_seen_yet)
        if msg_user_havent_seen_yet:
            #if not msg_user_havent_seen_yet.users_read_message.filter(user).first():
                check = True
                result += chat.title+' '
                result_ids += str(msg_user_havent_seen_yet.id)+' '
    if check:
        print(result+result_ids)
        http = HttpResponse(result+result_ids)
        http.status_code=200
        return http
    http = HttpResponse('')
    http.status_code = 204
    return http


@csrf_exempt
@login_required
def get_aes_key(request, url):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    chat = Chats.objects.filter(users=user, url=url).first()
    if request.method == 'POST':
        if not chat.secret_key:
            chat.secret_key = secrets.token_hex(256)
            chat.save()
            return HttpResponse(chat.secret_key)
        return HttpResponse(chat.secret_key)
    return HttpResponse('false')


def additional(request):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    if not auth:
        return redirect("../")
    user = Users.objects.filter(username=auth.username).first()
    if not user:
        return redirect("../")
    if not user.code or int(user.code)<1000:
        user.code = str(random.randint(1000, 9999))
        user.save()
    return render(request, 'additional.html', context={'username': None, 'code': user.code})
#
#
# BackgroundScheduler
#
#


def delete_null_chats():
    #threading.Timer(172000, delete_null_chats).start()
    chats = Chats.objects.filter(users=None)
    for chat in chats:
        Messages.objects.filter(chats=chat).delete()
    Chats.objects.filter(users=None).delete()
    return True


def remove_deleted_messages():
    #threading.Timer(172000, remove_deleted_messages).start()
    DeletedMessages.objects.all().delete()
    return True


def dis_online_users():
    #threading.Timer(33, dis_online_users).start()
    date_time_now = datetime.datetime.utcnow()
    users = Users.objects.filter(next_status_send__lt=date_time_now, is_online=True).all()
    if not users:
        print("ничего нет")
        close_old_connections()
        return True
    for user in users:
        user.is_online = False
        user.save()
    print("Выолнил")
    close_old_connections()
    return True


def delete_ovelimited_messages():
    chats = Chats.objects.all()
    for chat in chats:
        dt = datetime.datetime.utcnow()-datetime.timedelta(days=1)
        ms = Messages.objects.filter(chats=chat, senddate__lt=dt).all()
        for message in ms:
            CWOL = ChatsWithOverLimits.objects.filter(chat_url=chat.url).first()
            if not CWOL:
                CWOL = ChatsWithOverLimits(chat_url=chat.url)
                CWOL.save()
        Messages.objects.filter(chats=chat, senddate__lt=dt).all().delete()


scheduler = BackgroundScheduler()
scheduler.add_job(dis_online_users, 'interval', seconds=33)
scheduler.add_job(remove_deleted_messages, 'interval', minutes=120)
scheduler.add_job(delete_null_chats, 'interval', minutes=120)
scheduler.add_job(delete_ovelimited_messages, 'interval', minutes=120)
scheduler.start()
from uuid import uuid4
from datetime import timedelta
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import Context
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import Users, UsersAuth, is_authorized, Chats


# Create your views here.
def index(request):
    if 'token' in request.COOKIES:
        if is_authorized(request.COOKIES['token']):
            return redirect('/lk')
    if request.method == 'POST':
        if request.POST['token'] == '1':
            username = request.POST['username']
            password = request.POST['password']
            user = Users.objects.filter(username=username, password=password)
            if user:
                token = uuid4()
                usr = UsersAuth(username=username, token=token)
                usr.save()
                response = redirect('/lk')
                response.set_cookie(key='token', value=token, max_age=5184000)
                return response
            return render(request, 'regform.html', {'msg': ["Неверное имя пользователя или пароль!"]})
        else:
            username = request.POST['username']
            password = request.POST['password']
            firstname = request.POST['firstname']
            secondname = request.POST['secondname']
            email = request.POST['email']
            if Users.objects.filter(username=username).exists():
                return render(request, 'regform.html', {'msg': ['Такой пользователь уже существует. Пожалуйста, авторизируйтесь!']})
            user = Users(username=username, email=email, password=password, firstname=firstname, secondname=secondname)
            user.save()
            if user:
                token = uuid4()
                usr = UsersAuth(username=username, token=token)
                usr.save()
                #token = usr.login(username=username)
                response = redirect('/lk')
                response.set_cookie(key='token', value=token, max_age=5184000)
                return response
    else:
        return render(request, 'regform.html', context={})


def login_required(func):
    def wrapper(request):
        if not ('token' in request.COOKIES):
            return redirect('/')
        if not is_authorized(request.COOKIES['token']):
            return redirect('/')
        res = func(request)
        return res
    return wrapper


@login_required
def lk(request):
    auth = UsersAuth.objects.filter(token=request.COOKIES['token']).first()
    user = Users.objects.filter(username=auth.username).first()
    chats = Chats.objects.filter(users=user)
    render_chats_arr = []
    for index, chat in enumerate(chats):
        render_chat = {}
        render_chat["index"] = "files/images/"+str(index+1)+".jpg"
        render_chat["name"] = chat.title
        render_chat["url"] = chat.url
        render_chats_arr.append(render_chat)

    print(render_chats_arr)

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
    chat = Chats(title='TITLE'+str(uuid4()))
    chat.save()
    chat.users.add(user)
    chat.save()


def chatting(request):
    return HttpResponse('ok')


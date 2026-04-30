from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from chat.models import ChatRoom


def register(request):
    #регистрация пользователя
    if request.method == "POST": # проверяем является ли запрос ПОСТОМ
        form = RegisterForm(request.POST) # Если да то в форму передаем данные и сохроняем в переменную
        if form.is_valid():#проверка на правельно заполненую форму
            user = form.save()#сохроняем форму и добавляет пользователя в бд
            login(request, user)#выполянем вход пользователя
            return redirect('index')#возвращаем главное меню
    else:
        form = RegisterForm()#форма становится пустой
    return render(request, 'accounts/register.html', {'form': form})#перенапраляем на страницу с пустой формой



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Неверный email или пароль')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def index(request):
    # Получаем все комнаты
    rooms = ChatRoom.objects.all()
    
    return render(request, 'accounts/index.html', {
        'rooms': rooms
    })
    

def user_logout(request):
    logout(request)
    return redirect('index')
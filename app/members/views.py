from django.contrib.auth import login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render

from members.forms import LoginForm
from members.models import User

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('posts:post-list')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'members/login.html', context)


def signup_view(request):
    email = request.POST['email']
    username = request.POST['username']
    name = request.POST['name']
    password = request.POST['password']

    if User.objects.filter(username=username).exists():
        return HttpResponse('이미 사용중인 username입니다')
    if User.objects.filter(email=email).exists():
        return HttpResponse('이미 사용중인 email입니다')

    user = User.objects.create_user(
        password=password,
        username=username,
        email=email,
        name=name,
    )
    login(request, user)
    return redirect('posts:post-list')


def logout_view(request):
    logout(request)
    return redirect('members:login')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_http_methods,require_POST
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
# Create your views here.


@require_http_methods(['POST','GET'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    
    context = {
        "form" : form,
    }
    return render(request,'accounts/signup.html',context)


@require_http_methods(['POST','GET'])
def login(request):
    if request.method=='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    
    context = {
        'form':form,
    }
    return render(request,'accounts/login.html',context)


@require_POST
def logout(request):
    # 로그인 된 사용자라면
    if request.user.is_authenticated:
        auth_logout(request)
    
    return redirect('accounts:login')


@login_required
@require_http_methods(['POST','GET'])
def update(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method=='POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')

    else:
        form = CustomUserChangeForm(instance=request.user)
    
    context = {
        'form':form,
    }
    return render(request,'accounts/update.html',context)


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('articles:index')
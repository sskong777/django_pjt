from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('todos:index')

    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('todos:index')

    else:
        form = CustomUserCreationForm()
    
    context = {
        'form':form,
    }
    return render(request,'accounts/signup.html',context)


def login(request):
    if request.user.is_authenticated:
        return redirect('todos:index')
    if request.method=='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            form.save()
            auth_login(request, form.get_user())
            return redirect('todos:index')
    else:
        form = AuthenticationForm()
    
    context = {
        'form':form,
    }
    return render(request,'accounts/login.html',context)
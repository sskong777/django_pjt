from django.shortcuts import redirect, render,get_object_or_404

from todos.models import Todo
from .forms import TodoForm
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    todos = request.user.todo_set.all()
    # user = todos.user_set.all()
    context = {
        'todos':todos,
    }

    return render(request, 'todos/index.html', context)

def new(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')    
    
    if request.method =='POST':    
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.save()
            return redirect('todos:index')
    else:
        form = TodoForm()
    
    context={
        'form' : form,
    }
    return render(request,'todos/new.html',context)
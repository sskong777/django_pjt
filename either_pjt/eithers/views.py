from django.shortcuts import redirect, render,get_object_or_404
from eithers.forms import EitherForm,CommentForm
from .models import Either
# Create your views here.

def index(request):
    eithers = Either.objects.all()
    context = {
        'eithers' : eithers,
    }
    return render(request, 'eithers/index.html', context)


def create(request):
    if request.method == 'POST':
        form = EitherForm(request.POST)
        if form.is_valid():
            either = form.save()
            return redirect('eithers:detail', either.pk)
    else:
        form = EitherForm()

    context = {
        'form':form,
    }
    return render(request,'eithers/create.html',context)

    
def detail(request, either_pk):
    # either = Either.objects.get(pk=either_pk)
    either = get_object_or_404(Either,pk=either_pk)
    form = CommentForm()
    comments = either.comment_set.all()
    total = comments.count()
    
    # 방법 1.
    blue = comments.filter(pick='blue').count()
    red = comments.filter(pick='red').count()
    
    # 방법 2.
    # blue_cnt, red_cnt = 0,0
    # for comment in comments:
    #     if comment.pick == 'blue':
    #         blue_cnt += 1
    #     else:
    #         red_cnt += 1
    
    context = {
        'either' : either,
        'form' : form,
        'comments' : comments,
        'red_per' : round(red / total * 100, 2)if total else 0,
        'blue_per' : round(blue / total * 100, 2) if total else 0,
        
        
    }
    return render(request, 'eithers/detail.html',context)



def comment_create(request,either_pk):
    either = get_object_or_404(Either,pk=either_pk)
    if request.method=='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.either = either
            comment.save()
    return redirect('eithers:detail',either.pk)

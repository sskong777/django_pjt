# PJT06



### 이번 pjt 를 통해 배운 내용

* DB를 활용한 웹페이지 구현
* GET,POST 방식
* model과 form을 활용한 CRUD조작
* django의 MTV패턴
* form에 bootstrap적용
* Media File업로드

---

#  요구사항

커뮤니티 서비스의 게시판 기능 개발을 위한 단계로, 영화 데이터의 생성, 조회, 수정, 삭제 가능 한 어플리케이션을 완성합니다. 해당 기능은 향후 커뮤니티 서비스의 필수 기능으로 사용됩니다. 아래 기술된 사항들은 필수적으로 구현해야 하는 내용입니다. Django 프로젝트 이름은 pjt06, 앱 이름은 movies로 지정합니다.

## A. Model

* 정의할 모델 클래스의 이름은 Movie이며, 다음과 같은 정보를 저장합니다.

  ```python
  from distutils.command.upload import upload
  from django.db import models
  
  # Create your models here.
  class Movie(models.Model):
      title = models.CharField(max_length=20)
      audience = models.IntegerField()
      release_date = models.DateField()
      genre = models.CharField(max_length=30)
      score = models.FloatField()
      poster_url = models.ImageField(upload_to='images/',blank=True)
      description = models.TextField()
  
  ```
  
  * DB에 저장할 내용을 models.py class를 통해 만들어준다. 
  
  * models.py에 작성한 내용을 DB에 저장하고 반영하기 위해 두가지 명령어를 실행해야한다
  
    ```bash
    python manage.py makemigrations
    pyhton manage.py migrate
    ```
  
  * 각각의 항목별로 data_type을 지정하고 해당하는 항목에 맞는 조건을 인자로 받아 작성해줍니다.
  
  * poster_url에 이미지를 불러오기 위해 ImageField에 인자값으로 `upload_to='images/'`을
  
    주었고, `blank=True`로 기본값을 비어있는 형태로 만들어주었습니다.

----



## B.  URL

* pjt06/urls.py

  ```python
  from django.contrib import admin
  from django.urls import path, include
  from django.conf import settings
  from django.conf.urls.static import static
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('movies/', include('movies.urls')),
  ]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
  
  ```
  
  * 프로젝트 바로 밑의 urls.py에서 app별로 url분리를 해주기 위해 include('app명.urls')로 분리를 해주었습니다.
  * `+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)` 이 부분으로  미디어 파일의 경로를 지정해주었습니다.

  ```python
  #처음에 
  from django.conf import settings
  from django.conf.urls.static import static
  #과
  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
  #이 부분을 앱 안의 urls.py에 지정을 해주어서 페이지에 이미지 파일이 나타나지 않았는데 설정을 하였을 때 프로젝트의 루트 위치로 경로를 지정해주어서 앱 밑의 urls.py에서 작성하였을 때는 경로가 잘못지정되어 이미지 파일이 나타나지 않았다.
  ```
  
  
  
* movies/urls.py

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'movies'
  urlpatterns = [
      path('', views.index, name='index'),
      path('create/', views.create, name='create'),
      path('<int:movie_pk>/',views.detail,name='detail'),
      path('<int:movie_pk>/update/', views.update, name='update'),
      path('<int:movie_pk>/delete/',views.delete, name='delete'),
  ]
  ```
  
  * url.py에서 작성하여 views.py에 각 함수를 호출 하면 해당 주소를 보여줄 html을 render하여 페이지를 보여준다. 

  * context에 저장된 데이터를  html에서 DTL(Django Templates Language)을 이용하여 요청받은 정보를 표현한다. 

  * app_name과 각 url_pattern의 name을 통해 접근하기 위해 값을 정해준다.

  * id값을 통한 variabel routing을 하기 위해 자료형:variable변수명으로 url값을 설정한다.

    

---



## C. Admin 

* 요구 사항 : 위에서 정의한 모델 Movie을 Admin site에 등록합니다. MovieAdmin 클래스를 작성하며 등록 후 Admin site에서 데이터의 생성, 조회, 수정, 삭제가 가능해야 합니다. 

* admin.py

  ```python
  from django.contrib import admin
  from .models import Movie
  # Register your models here.
  
  admin.site.register(Movie)
  ```


---





## D.  View

![image-20220311170700049](readme.assets/image-20220311170700049.png)

```python
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_safe, require_POST,require_http_methods
from .models import Movie
from .forms import MovieForm


# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }

    return render(request, 'movies/index.html', context)

@require_http_methods(['POST','GET'])
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()

    context = {
        'form': form,

    }

    return render(request, 'movies/create.html', context)

@require_safe
def detail(request, movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie' : movie,
    }

    return render(request,'movies/detail.html',context)


@require_http_methods(['POST','GET'])
def update(request,movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie,pk=movie_pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save()
        return redirect('movies:detail',movie.pk)
    else:
        form = MovieForm(instance=movie)
    
    context ={
        'form' : form,
        'movie' : movie,
    }
    return render(request,'movies/update.html',context)


@require_POST
def delete(request,movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie,pk=movie_pk)

    # if request.method == 'POST':/
    movie.delete()
    return redirect('movies:index')
    
    # return redirect('movies:detail', movie_pk)

```

* index함수는 모든 영화의 정보를 나타내야하므로 Movie.objects.all() 을 통해 DB에 저장된 전체 영화 정보들을 가져와 context에 담아준다. 이 때 require_safe 데코레이터를 통해 안전한 method로 정보를 가져와준다.

  

* create함수는 POST일 때 동작을 하게 작성을 하였다. 사용자의 입력을 받아 DB에 저장해주는 과정이기 때문에 POST방식으로 정보를 받아야 한다. POST방식이 아닐 때는 다시 작성하는 폼인 create페이지로 돌아가도록 return render를 해주었다.  

  * context를 else바깥에 작성한 이유

    ```
    첫 if문에서 유효성 검사를 실패하면 create페이지로 렌더시켜줘야하는데 만약에 context구문이 else문 안에들어가면 유효성 검사 실패 시 form을 받아줄 content가 없기 떄문에
    POST방식이 아닐떄를 처리하는 else구문과 같은 레벨에 작성되어야합니다.
    ```

  * if 조건 문에 POST가 먼저 온 이유

    ```
    request의 메소드는 get,post말고도 다른 방식이 있기 때문에 if에서 POST인지를 확인하고 else에서 POST가 아닌 다른 방식으로 올때의 처리를 해줘야합니다.
    만약에 GET을 if문에서 처리를 해주고 POST에 대한 처리가 else로 빠진다면 else구문에서는 GET과POST가 아닌 방식으로 요청이 될 때의 처리가 어려워집니다. 만약 그럴 경우에는 elif문으로 각각의 요청을 따로 처리를 해줘야합니다.
    ```

  * require_http_methods에 리스트로 POST와 GET을 받아 POST와 GET일 때만 웹페이지가 동작하게 데코레이션 함수를 작성하였다.

    

* detail함수는 url로 전달받은 pk값에 movie의 id값과 매칭하여 pk값에 해당하는 movie의 id값을 통해 객체를 생성하여 하나의 영화를 저장해준다.

  ```python
  movie = get_object_or_404(Movie, pk=movie_pk)
  ```

  get_object_or_404로 Movie와 pk값을 받아 에러가 발생했을때 그 에러 페이지를 보여줄 수 있도록 작성하였다.

  

* update는 create함수와 비슷한 방식을 작성하여 db에 저장시켜준다.

  * create함수와 다른 점은 pk값으로  그 값에 해당하는 데이터를 가져와 저장하는 방식이다.

    

* delete는 id값에 해당하는 영화를 다음과 같은 방식으로 삭제와 동시에 DB에 반영해준다.

      movie = get_object_or_404(Movie, pk=pk)
      movie.delete()

  * 1번째 방법 - if문으로 POST 인지 확인

    ```python
    def delete(request,movie_pk):
        movie = Movie.objects.get(pk=movie_pk)
    
        if request.method == 'POST':
        	movie.delete()
        	return redirect('movies:index')
        
        return redirect('movies:detail', movie_pk)
    ```

  * 2번째 방법 - 데코레이터 사용

    ```python
    @require_POST
    def delete(request,movie_pk):
        movie = get_object_or_404(Movie,pk=movie_pk)
    
        movie.delete()
        return redirect('movies:index')
    ```

---



## E.  Form

```python
from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    GENRE_1 = "comedy"
    GENRE_2 = "horror"
    GENRE_3 = "romance"
    GENRE_CHOICES = [
        (GENRE_1, "comedy"),
        (GENRE_2, "horror"),
        (GENRE_3, "romance"),
    ]
    genre = forms.ChoiceField(choices=GENRE_CHOICES, widget=forms.Select())

    score = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                'min': '0',
                'max': '5',
                'step': '0.5',
            }
        )        
    )

    release_date = forms.DateTimeField(
        # input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'type':'date',

            # 'class': 'form-control datetimepicker-input',
            # 'data-target': '#datetimepicker1'
        })
    )

    class Meta:
        model = Movie
        fields = '__all__'
```

* MovieForm 클래스를 작성하고 그 안에 inner class인 Meta를 작성하여 field의 모든 값을 넘겨준다.

* 이 Forms.py에서는 3가지 위젯을 사용하였다

  * select

  ```python
  GENRE_1 = "comedy"
  GENRE_2 = "horror"
  GENRE_3 = "romance"
  GENRE_CHOICES = [
      (GENRE_1, "comedy"),
      (GENRE_2, "horror"),
      (GENRE_3, "romance"),
  ]
  genre = forms.ChoiceField(choices=GENRE_CHOICES, widget=forms.Select())
  ```

  * NumberInput

  ```python
  score = forms.FloatField(
      widget=forms.NumberInput(
          attrs={
              'min': '0',
              'max': '5',
              'step': '0.5',
          }
      )        
  )
  ```

  * DateTimeField

  ```python
      release_date = forms.DateTimeField(
          widget=forms.DateInput(attrs={
              'type':'date',
          })
      )
  ```

  



## F.  Template

##### 	A.공유 템플릿 (base.html) 

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
  <title>Document</title>
</head>
<body>
  
  <div class="container">
    {% block content %}
    
    {% endblock content %}
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
</body>
</html>
```



B. 전체 영화 목록 조회 템플릿 (index.html)

![image-20220408201639862](readme.assets/image-20220408201639862.png)

```django
{% extends 'base.html' %}

{% block content %}
<h1>INDEX</h1>
<a href="{% url 'movies:create' %}">CREATE</a>
<hr>
{% for movie in movies %}
<p><a href="{% url 'movies:detail' movie.pk %}">{{movie.title}}</a></p>
<p>{{movie.score}}</p>
<hr>
{% endfor %}
<hr>

{% endblock content %}
```

* views.py에서 context에 담은 movies 정보를 사용하여 index페이지를 작성하였다.
* movies에는 DB에 저장된 모든 데이터가 들어있기 때문에 for문으로 저장된 데이터들을 출력해주어야한다. 위 명세서에서는 제목과 평점만 페이지에 나타내면 되기 때문에 해당하는 값들을 표시해주었다.



C. 영화 상세 정보 페이지 (detail.html)

![image-20220408201730588](readme.assets/image-20220408201730588.png)

```django
{% extends 'base.html' %}
{% load static %}
{% block content %}
<h1>DETAIL</h1>
<hr>
<div class="card" style="width: 18rem;">
  {% if movie.poster_url %}
    <img src="{{ movie.poster_url.url }}" class="card-img-top" alt="{{ movie.poster_url }}">
  {% endif %}
  <div class="card-body">
    <h5 class="card-title">{{ moive.title }}</h5>
    <p class="card-text">Audience : {{ movie.audience }}</p>
    <p class="card-text">Release Dates : {{ movie.release_date }}</p>
    <p class="card-text">Genre : {{ movie.genre }}</p>
    <p class="card-text">Score : {{ movie.score}}</p>
    <p class="card-text">{{ movie.description }}</p>
    
    <div class='d-flex'>
      <a href="{% url 'movies:update' movie.pk %}" class="btn btn-info">UPDATE</a>
      <form action="{% url 'movies:delete' movie.pk %}" method='POST'>
        {% csrf_token %}
        <button type="submit" class="btn btn-danger ms-2">
          DELETE
        </button>
      </form>
    </div>

  </div>
</div>
<a href="{% url 'movies:index' %}" class="btn btn-warning">BACK</a>
{% endblock content %}

```

* detail.html에서는 poster_url에 이미지를 불러오는데 어려움이 있었다.

* movie.poster_url필드에서 url을 가져와야한다.

  

##### 	D. 영화 작성 페이지 (create.html)	

![image-20220408201609135](readme.assets/image-20220408201609135.png)

```django
{% extends 'base.html' %}
{% load bootstrap5 %}
{% block content %}
<h1>CREATE</h1>
<form action="{% url 'movies:create' %}" method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {% bootstrap_form form %}

  {% buttons %}
    <button type="submit" class="btn btn-primary">
      Submit
    </button>
  {% endbuttons %}

</form>
<hr>

<a class="btn btn-info" href="{% url 'movies:index' %}">BACK</a>
{% endblock content %}

```

* create에서 POST방식으로 정보를 넘겨주어야 한다.  이 때 미디어 파일도 함께 넘겨줘야하기 때문에 `enctype="multipart/form-data"`도 함께 작성해주어야한다.
* 또한 bootstrap5를 설치하여 form을 좀 더 깔끔하게 저장할 수 있다. 에러메시지도 자동으로 같이 표시되었다.

##### 	E. 영화 수정 페이지 (update.html)

![image-20220408201754791](readme.assets/image-20220408201754791.png)

```django
{% extends 'base.html' %}
{% block content %}
<h1>UPDATE</h1>
<hr>
<form action="" method="POST">
  {% csrf_token %}
  {{ form.as_p}}
  <button>Submit</button>

  <hr>
  <a href="{% url 'movies:detail' movie.pk %}" class="btn btn-info">BACK</a>
{% endblock content %}
```

* POST방식으로 데이터를 보내야하기 때문에 csrf토큰을 꼭 넣어주어야한다. 

---





# 후기

* 저번 프로젝트와 유사한 부분이 많았지만 이번 프로젝트에는 models뿐만 아니라 forms.py로 데이터를 좀 더 쉽게 저장하고 쉽게 불러올 수 있었다. models.py만 작성했을 때는 필드의 수가 많으면 많을 수록 코드가 길어졌지만 form으로 구현하면  한 줄로 모든 필드를 작성할 수 있어서 정말 간편하였다.

  

* 이번에 처음으로 데코레이터와 미디어를 다루었는데, 데코레이터를 사용하니 더 편하게 method를 거를 수 있어서 편하였다. 정말 편한 기능인 것 같다. 또한 미디어에 대한 오류에 시간을 가장 많이 소비하였는데 단순 경로를 잘못지정해서였다. 이런 사소한 실수로 에러메시지를 긴 시간동안 봐야했지만 사소한 실수가 미디어 경로에 대한 제대로 된 이해가 없었기 때문에 일어났다고 생각했다. 어려운 부분이지만 다음에 실수하지 않도록 더 깊게 이해를 해야겠다.



* 또한 본격적으로 DB를 다루는 프로젝트라 정말 재밌고 남는 것이 있던 프로젝트였다. 또한 첫 페어프로그래밍으로 한 프로젝트여서 더 의미 있었다.  시간은 좀 더 오래걸리지만 혼자 할 때와는 또 다른 배울점이 있었고 더 재미있게 프로젝트를 진행할 수 있었다.



* 저번 프로젝트에는 에러페이지를 매우 많이 보았고, 그 이유로는 오타도 많았고, 경로설정과 같이 기본적인 부분에서 실수가 많았지만 이번 프로젝트는 페어프로그래밍으로 코더와 네이게이터로 팀을 이루어 진행을 하여 확실히 에러를 해결하는 시간이 빨랐고, 오타와 실수도 현저히 줄어든 것이 느껴졌던 프로젝트이다.



* 이번 프로젝트에는 bootstrap5를 install해서 진행을 하였는데 적용하는 방법도 훨씬 간편하였고 적용한 뒤의 페이지가 훨씬 깔끔하고 가독성이 좋아서 더 완성적인 느낌을 주었다.

  

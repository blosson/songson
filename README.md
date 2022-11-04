# README - BY. 송진주, 손민혁

- get_user_model()가 정확히 어떤 역할을 하는지?
- jsonResponse → context로 해당 정보를 넘겨줌
- 자바스크립트에서 설정한 변수값을 어떻게 html화면에서 띄울것이냐??  {{ 변수명 }} →>> 안됨.. 그래서 html에 태그를 만들고 태그나 class나 id를 설정해서 document.select~~ 한다음 innerText로 값을넣어준다.
    - DTL에 {{ person.followers.all|length }} 이걸 태그 안에 안 넣어주면 초기값이 없음. (초기 값이 필요없는 경우에는 안 써도됨. 그래서 우린 빼버림 ~~ 왜냐면 우린 js에서 innertext로 넣어줄 거거든~~)
- 객체.필드명.count() : 갯수 세어주는 메서드
- button 태그와 input태그는 다르다! input은 value 속성으로 값을 변경할 수 있지만 button은 설정한 다음 innerText로 해야함!

<like>

- 게시물에 대한 좋아요를 출력할 때 각 게시물마다 form태그가 하나씩 있으므로 id값을 매번 다르게 설정해주어야 한다!!! 그래서 id값 뒤에 {{ [blabla.pk](http://blabla.pk) }} 이런식으로 넣어줌. 여기서 공백이 있으면 안됨

```jsx
html
----
<button id="like-button-{{ review.pk }}">좋아요 취소</button>
      {% else %}
        <button id="like-button-{{ review.pk }}">좋아요</button>]

script
----

const likeBtn = document.querySelector(`#like-button-${reviewId}`)
```

- index 페이지에는 모든 게시물이 보이는데 이에 대한 좋아요를 각각 출력해주기 위해서는 selectAll을 해서 다 가져오고 콜백함수 forEach를 사용해서 각 게시물에 접근!!!

```jsx
<script>
    const likeForms = document.querySelectorAll(".like-forms")

    likeForms.forEach((likeform) => { blabla~~~
```

- follow수, like수 count할 때 —- if문을 넘긴 후에 변수를 설정해주고 context에 넘겨주어야 한다. 안그러면 if문 전의 결과로 넘겨주기 때문

```python
---- 좋은 예
if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            is_liked = False
        else:
            review.like_users.add(user)
            is_liked = True
---
        like_count = review.like_users.count()
---     
        context = {
            'is_liked': is_liked,
            'like_count': like_count,
        }
        return JsonResponse(context)

---- 안 좋은 예

if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user
---
			  like_count = review.like_users.count()
---
        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            is_liked = False
        else:
            review.like_users.add(user)
            is_liked = True

        
        context = {
            'is_liked': is_liked,
            'like_count': like_count,
        }
        return JsonResponse(context)
```

- movie에서 genre가져와서 출력하기
    - 원래 json movie 파일에는 장르 데이터가 없었다.
    - 그런데 movie의 정보와 genre의 정보가 따로 저장되어 있어서 >>> manyTomany 필드로 무비 모델 안에 장르 필드를 넣어줬다.
    - JSON의 movie 파일을 보니까 다른 것들은 전부 int나 string이고 1개씩 있어서 바로 불러올 수 있었지만, genre는 리스트로 되어 있어서 아무리 개수가 1개여도 그래도 가져오면 `none`값을 출력해줘서 매우 화가 났었다.
    - 하지만 준형좌와 영민좌의 말에 따르면 리스트를 출력할 때는 값이 한개여도 반드시 객체.필드명.all 을 사용해야 출력할 수 있다는 것이다.
    - 그래서 (1개 영화에 여러 장르가 있을 수도 있으므로) HTML에서 for문으로 돌려서 출력해주면 된다!!!
    - 하…

```python

--- view.py 

def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    # genre = movie.genres.all()
    context = {
        'movie': movie,
        # 'genre': genre,
    }
    return render(request, 'movies/detail.html', context)

--- detail.html
{% for each_genre in movie.genres.all %}
  {{ each_genre.name }}
{% endfor %}

--- JSON 파일
"genres": [
        10749
      ]
```

- 리스트 안에서 딕셔너리의 특정 키값으로 정렬하기
    - 람다함수를 사용해서 하나의 객체(x)의 key 값 (vote_average)에 접근!!! 해서 정렬하기
    - 그냥 바로 key=vote_average로 사용하면 인식하지 못해서 비교가 안됨.

```python
def recommended(request):
    user = request.user
    movies = Movie.objects.all()
    if user.is_authenticated:
        random_num = []
        for _ in range(30):
            random_num.append(randint(1, 201))
        movie_list = []
        for i in random_num:
            for movie in movies:
                if i == movie.pk:
                    movie_list.append(movie)
--------
        sort_key = lambda x:x.vote_average
        movie_list = sorted(movie_list, key=sort_key)[30:20:-1]
        # movie_list = movie_list.order_by('-vote_average')[:10]
--------
        context = {
            'movie_list': movie_list,
        }
        return render(request, 'movies/recommended.html', context)
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4e50d940-65a5-4631-8848-2be7923e1adc/Untitled.png)
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Post
from blog import models as django_models, models
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.utils import timezone

from blog import models as django_models, utils as django_utils
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET, require_http_methods


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 3


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


def post_detail(request, slug):
    template_name = "post_detail.html"
    object_list = django_models.Post.objects.all()
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None

    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            'object_list': object_list,
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )

# найти библеотеку котор из кирилиц (из тайтла) делает латитницу
# отказаться от слагов , вместо него айди
def create_post(request):
    if request.method == "GET":
        return render(request, "post_create.html")
    elif request.method == "POST":
        title = request.POST.get("title", "")
        slug = request.POST.get("slug", "")
        content = request.POST.get("content", "")

        models.Post.objects.create(
            title=title,
            content=content,
            slug=slug,
            author_id=True

        )

        return redirect(reverse('home'))


#
# class PostCreate(View):
#
#     def post(self, request):
#         bound_form = PostForm(request.POST)
#         if bound_form.is_valid():
#             new_post = bound_form.save()
#             return redirect(new_post)
#         return render(request, 'post_create.html', context={'form': bound_form})


# def post_detail_img(request):
#     object_list = django_models.Post.objects.all()
#
#     return render(request, 'post_detail.html', context={'object_list': object_list})


def contacts(request):
    context = {}
    return render(request, 'contacts.html', context=context)


def home(request):
    object_list = django_models.Img.objects.all()

    return render(request, 'home.html', context={'object_list': object_list})


def home_post(request):
    object_list = django_models.Img.objects.all()
    return render(request, 'img_detail.html', context={'object_list': object_list})


# class HomePageView(ListView):
#     model = Img
#     template_name = 'home.html'
#     success_url = reverse_lazy('index')


# class DetailPostView(ListView):
#     model = Img
#     form_class = PostForm
#     template_name = 'img_detail.html'
#     success_url = reverse_lazy('img')


def main(request):
    return render(request, 'main.html')


@login_required
@django_utils.logging_txt_decorator
def rating_like(request, post_id=None):
    # post = django_models.Post.objects.get(id=post_id)
    # user = request.user
    #
    # try:
    #     _rating = django_models.PostRatingModel.objects.get(post=post, user=user)
    #     like = _rating
    #     if like.is_like is True:
    #         like.delete()  # todo ЕСЛИ В БАЗЕ УЖЕ СТОИТ ЛАЙК
    #     else:
    #         like.is_like = True
    #         like.save()  # todo ЕСЛИ В БАЗЕ УЖЕ СТОИТ ДИЗЛАЙК
    # except Exception as error:
    #     django_models.PostRatingModel.objects.create(
    #         user=user,
    #         post=post,
    #         is_like=True,
    #     )  # todo ЕСЛИ В БАЗЕ НЕТУ ОТМЕТКИ
    #     return render(request, 'post_detail.html')
    #
    # return redirect(reverse("post_detail", args=(post.slug,)))

    post = django_models.Post.objects.get(id=post_id)
    user = request.user

    _rating = django_models.PostRatingModel.objects.filter(post=post, user=user)
    if _rating.count() < 1:
        django_models.PostRatingModel.objects.create(
            user=user,
            post=post,
            is_like=True,
        )  # todo ЕСЛИ В БАЗЕ НЕТУ ОТМЕТКИ
    else:
        like = _rating[0]
        if like.is_like is False:
            like.is_like = True
            like.save()  # todo ЕСЛИ В БАЗЕ УЖЕ СТОИТ ЛАЙК
        else:
            like.delete()  # todo ЕСЛИ В БАЗЕ УЖЕ СТОИТ ДИЗЛАЙК
            return render(request, 'error_likes.html')

    return redirect(reverse("post_detail", args=(post.slug,)))


@login_required
@django_utils.logging_txt_decorator
def rating_dislike(request, post_id=None):
    post = django_models.Post.objects.get(id=post_id)
    user = request.user

    _rating = django_models.PostRatingModel.objects.filter(post=post, user=user)
    if _rating.count() < 1:
        django_models.PostRatingModel.objects.create(
            user=user,
            post=post,
            is_like=False,
        )  # todo ЕСЛИ В БАЗЕ НЕТУ ОТМЕТКИ
    else:
        like = _rating[0]
        if like.is_like is True:
            like.is_like = False
            like.save()  # todo ЕСЛИ В БАЗЕ УЖЕ СТОИТ ЛАЙК
        else:
            like.delete()  # todo ЕСЛИ В БАЗЕ УЖЕ СТОИТ ДИЗЛАЙК
            return render(request, 'error_dislike.html')

    return redirect(reverse("post_detail", args=(post.slug,)))


def login_f(request):
    if request.method == 'GET':
        return render(request, 'profile_login.html', context={})
    elif request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is None:
                return render(request, 'profile_login.html', context={"error": "User не найден"})
            login(request, user)
            return redirect('main')
        return render(request, 'profile_login.html', context={"error": "username or password пустые"})


def register_f(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "profile_register.html", context={})

    elif request.method == "POST":
        # todo чтение из формы
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        # todo чтение из формы

        # todo сравнение паролей
        if password1 != password2:
            return render(request, "profile_register.html", context={"error": "incorrect password1"})
        # todo сравнение паролей

        # todo регистрация пользователя
        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        # todo регистрация пользователя

        # todo перенаправление пользователя
        return redirect("login")
        # todo перенаправление пользователя


def logout_f(request):
    logout(request)
    return redirect('main')


def search(request):
    search_query = request.GET.get('search', '')
    if search_query:
        todos = Post.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    else:
        todos = Post.objects.all()

    return render(request, 'index.html', {'post_list': todos})


def profile(request):
    return render(request,
                  'profile.html',
                  )


def delete_post(request, slug):
    Post.objects.get(slug=slug).delete()
    return redirect(reverse("home"))


def admin_all(request):
    users = User.objects.filter(is_superuser=True)
    user = User.objects.filter(is_active=True)
    return render(request,
                  'profile_admin_all.html',
                  {
                      "user_all": user,
                      "user_admin": users,
                  },
                  )

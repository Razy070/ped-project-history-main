from django.urls import include, path

from . import views
from .feeds import AtomSiteNewsFeed, LatestPostsFeed


# from .views import DetailPostView

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('admin_all/', views.admin_all, name='admin_all'),

    path('create_post/', views.create_post, name='create_post'),

    path('search/', views.search, name='search'),


    path('login/', views.login_f, name='login'),
    path('login/', views.login_f, name='category_list'),
    path('register/', views.register_f, name='register'),
    path('logout/', views.logout_f, name='logout'),

    path('delete_post/<slug:slug>', views.delete_post, name='delete_post'),

    path('home/', views.home, name='index'),
    path('post_home/', views.home_post, name='img'),

    path("post/<int:post_id>/rating/like/", views.rating_like, name="rating_like"),
    path("post/<int:post_id>/rating/dislike/", views.rating_dislike, name="rating_dislike"),

    # path('post/<int:pk>/rating/', views.post_rating, name='post_rating'),
    # path('home/', HomePageView.as_view(), name='index'),
    # path('img_detail', views.img_detail, name='img'),
    # path('detail/', DetailPostView.as_view(), name='img'),
    path("contacts/", views.contacts, name="contacts"),
    path("", views.main, name="main"),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("main/", views.PostList.as_view(), name="home"),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("<slug:slug>", views.post_detail, name="post_detail"),
]

from django.urls import include, path

from . import views
from .feeds import AtomSiteNewsFeed, LatestPostsFeed
from .views import MyProfile

urlpatterns = [
    # path('profile/', views.profile, name='profile'),
    path('admin_all/', views.admin_all, name='admin_all'),

    path('create_post/', views.create_post, name='create_post'),

    path('search/', views.search, name='search'),

    path('profile/', MyProfile.as_view(), name='profile'),

    path('login/', views.login_f, name='login'),
    path('login/', views.login_f, name='category_list'),
    path('register/', views.register_f, name='register'),
    path('logout/', views.logout_f, name='logout'),

    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),


    path("post/<int:post_id>/rating/like/", views.rating_like, name="rating_like"),
    path("post/<int:post_id>/rating/dislike/", views.rating_dislike, name="rating_dislike"),

    path("contact", views.contact, name="contact"),
    path("contact_successfully", views.contacts_successfully, name="contacts_successfully"),


    path("", views.main, name="main"),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("main/", views.PostList.as_view(), name="home"),

    path("post_detail/<int:post_id>", views.post_detail, name="post_detail"),
]

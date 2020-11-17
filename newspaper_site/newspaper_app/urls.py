from django.contrib import admin
from django.urls import path
from . import views
app_name = "newspaper_app"
urlpatterns = [
    path("", views.Articles_view, name="index"),
    path("profile/", views.Profile_initial_render, name="profile"),
    path("profile_view/", views.Profile_view, name="profile_view"),
    path("profile_update/", views.Profile_put, name="profile_update"),
    path("article/<int:id>/", views.Article_view, name="article"),
    path("like_view/<int:article_id>/", views.Like_view, name="like_view"),
    path("like_delete/<int:like_id>/", views.Like_delete, name="like_delete"),
    path("like_post/", views.Like_post, name="like_post"),
    path("comment_view/<int:article_id>/",
         views.Comment_view, name="comment_view"),
    path("comment_post/", views.Comment_post, name="comment_post"),
    path("comment_edit/", views.Comment_put, name="comment_edit"),
    path("comment_delete/<int:comment_id>/",
         views.Comment_delete, name="comment_delete"),
    path('register_validation/', views.register_validation,
         name="register_validation"),
    path('register/', views.register_view, name="register_form"),
    path('login_validation/', views.login_validation, name="login_validation"),
    path('login/', views.login_view, name="login_form"),
    path('logout/', views.logout_view, name="logout")
]

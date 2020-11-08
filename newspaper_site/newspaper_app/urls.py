from django.contrib import admin
from django.urls import path
from . import views
app_name = "user"
urlpatterns = [
    path("", views.index, name="base"),
    path('register_validation/', views.register_validation,
         name="register_validation"),
    path('register/', views.register_view,
         name="register_form"),
    path('login_validation/', views.login_validation,
         name="login_validation"),
    path('login/', views.login_view,
         name="login_form"),
    path('logout/', views.logout_view,
         name="logout")
]

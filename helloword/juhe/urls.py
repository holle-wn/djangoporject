from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('qq', views.qq),
    path('image', views.image),
    path('image1', views.Image.as_view()),
    path('jack', views.jack),
    path('testcookie', views.TestCookie.as_view()),
    path('testcookie1', views.TestCookie1.as_view()),
    path('authorize', views.Authorize.as_view()),
    path('user', views.User.as_view()),
    path('logout', views.Logout.as_view()),
    path('status', views.Status.as_view()),
    path('weather', views.Weather.as_view()),
]
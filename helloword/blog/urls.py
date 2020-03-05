from django.urls import path, include

from . import views

urlpatterns = [
    path('index', views.article1, name='index'),
    path('detail/<int:article_id>', views.detail, name='detail')
]

# handler404 = 'blog.views.not_found'

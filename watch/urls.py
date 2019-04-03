from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('watch', views.watch_games, name='watch'),
]

from django.urls import path, include
from . import views
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('watch', views.watch_games, name='watch'),
    path('', views.index, name='index'),

]

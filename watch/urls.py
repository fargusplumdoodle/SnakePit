from django.urls import path, include
from . import views
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('docs', views.docs, name='docs'),
    path('', views.index, name='index'),
]

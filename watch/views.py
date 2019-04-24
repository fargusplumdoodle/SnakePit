from django.shortcuts import render, redirect
import json
from data.models import Game, Turn
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='accounts/login/')
def index(request):
    content = {
        'api_url': request.build_absolute_uri('/'),
        'username': request.user
    }
    return render(request, 'watch/watch_games.html', content)


def docs(request):
    return render(request, 'watch/docs.html', {})

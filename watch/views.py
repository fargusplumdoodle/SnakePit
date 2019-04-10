from django.shortcuts import render, redirect
import json
from data.models import Game, Turn
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

data = {
    "you": {
        "health": 79,
        "body": [
            {
                "y": 6,
                "x": 6
            },
            {
                "y": 6,
                "x": 5
            },
            {
                "y": 6,
                "x": 4
            },
            {
                "y": 6,
                "x": 3
            }
        ],
        "name": "SekhnetSnek",
        "id": "582365c9-cc9a-4fc5-93f1-a5a3fb533167"
    },
    "turn": 30,
    "board": {
        "snakes": [
            {
                "health": 98,
                "body": [
                    {
                        "y": 3,
                        "x": 2
                    },
                    {
                        "y": 2,
                        "x": 2
                    },
                    {
                        "y": 2,
                        "x": 3
                    },
                    {
                        "y": 2,
                        "x": 4
                    },
                    {
                        "y": 3,
                        "x": 4
                    },
                    {
                        "y": 4,
                        "x": 4
                    },
                    {
                        "y": 5,
                        "x": 4
                    },
                    {
                        "y": 5,
                        "x": 3
                    },
                    {
                        "y": 4,
                        "x": 3
                    }
                ],
                "name": "Son of Robosnake",
                "id": "24b8fc5a-8aec-42ed-b8df-42ed6bb11003"
            },
            {
                "health": 79,
                "body": [
                    {
                        "y": 0,
                        "x": 2
                    },
                    {
                        "y": 1,
                        "x": 2
                    },
                    {
                        "y": 1,
                        "x": 3
                    },
                    {
                        "y": 0,
                        "x": 3
                    }
                ],
                "name": "SekhnetSnek",
                "id": "582365c9-cc9a-4fc5-93f1-a5a3fb533167"
            }
        ],
        "width": 7,
        "height": 7,
        "food": [
            {
                "y": 0,
                "x": 6
            },
            {
                "y": 5,
                "x": 1
            },
            {
                "y": 2,
                "x": 6
            },
            {
                "y": 4,
                "x": 1
            },
            {
                "y": 1,
                "x": 6
            },
            {
                "y": 5,
                "x": 6
            },
            {
                "y": 4,
                "x": 2
            }
        ]
    },
    "game": {
        "id": "a54f-3842-476b-80a7-4455934edddd2fc"
    }
}

valid_data = {'you': {'health': 79, 'body': [{'y': 600, 'x': 600}, {'y': 600, 'x': 500}, {'y': 600, 'x': 400}, {'y': 600, 'x': 300}], 'name': 'SekhnetSnek', 'id': '582365c9-cc9a-4fc5-93f1-a5a3fb533167', 'head': {'y': 600, 'x': 600}}, 'turn': 30, 'board': {'snakes': [{'health': 98, 'body': [{'y': 300, 'x': 200}, {'y': 200, 'x': 200}, {'y': 200, 'x': 300}, {'y': 200, 'x': 400}, {'y': 300, 'x': 400}, {'y': 400, 'x': 400}, {'y': 500, 'x': 400}, {'y': 500, 'x': 300}, {'y': 400, 'x': 300}], 'name': 'Son of Robosnake', 'id': '24b8fc5a-8aec-42ed-b8df-42ed6bb11003', 'head': {'y': 300, 'x': 200}}], 'width': 700, 'height': 700, 'food': [{'y': 0, 'x': 600}, {'y': 500, 'x': 100}, {'y': 200, 'x': 600}, {'y': 400, 'x': 100}, {'y': 100, 'x': 600}, {'y': 500, 'x': 600}, {'y': 400, 'x': 200}]}, 'game': {'id': 'a54f-3842-476b-80a7-4455934edddd2fc'}}


# @login_required(login_url='accounts/login/')
def index(request):
    content = {'api_url': request.build_absolute_uri('/') + 'games/snake'}
    return render(request, 'watch/watch_games.html', content)


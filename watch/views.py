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


def index(request):
    # this is so we can access all of the data from javascript
    # new_data = {'data': data}
    return render(request, 'watch/index.html', load_recent_game_from_database())


@login_required(login_url='accounts/login/')
def watch_games(request):
    return render(request, 'watch/watch_games.html', load_recent_game_from_database())


def load_recent_game_from_database():
    """
    This loads the most recent game stored in the database and returns it in a dictionary ready for passing to index
    :return: dictionary
    """
    # generating base skeleton
    content = {
        'width': None,
        'height': None,
        'gid': None,
        'turn': []
    }

    print(Game.objects.all())

    # Ok this looks weird but it gets the most recent game, trust me
    for x in Turn.objects.filter(game=Game.objects.filter(gid=Game.objects.all().order_by('-id')[0].gid)[0]):
        content['turn'].append(json.loads(x.data))

    # getting base info of game
    content['width'] = content['turn'][0]['board']['width']
    content['height'] = content['turn'][0]['board']['height']
    content['gid'] = content['turn'][0]['game']['id']

    content = {'data': content}
    return content


def load_database_from_game(gameDir='/home/fargus/Projects/Battlesnake/saves/2019-02-12_dfb9/'):
    """
    This will load a game into the database with correct values
    No error checking is performed, it assumes that each file in the specified
    directory contains valid json from the same game
    :param gameDir: a directory filled with turns from a game
    """
    import os

    # changing directory to gameDir
    os.chdir(gameDir)
    # getting all files in gameDir based on the time they were modified
    file_names = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime)

    # fixing file names to be the full path
    files = []
    for fl in file_names:
        files.append(gameDir + fl)

    # loading all turns into array
    allTurns = []
    for fl_name in files:
        fl = open(fl_name, 'r')
        data = json.loads(fl.read())
        allTurns.append(data)

    # getting game data from first turn
    gid = allTurns[0]['game']['id']
    width = allTurns[0]['board']['width']
    height = allTurns[0]['board']['height']

    # new game
    game = Game(gid=gid, width=width, height=height)
    game.save()

    # creating turns
    for turnData in allTurns:
        turn = Turn(turnNo=turnData['turn'], game=game, data=json.dumps(turnData))
        turn.save()


def sanitize_api2019(data, mod=100):
    """This function is for sanitizing data so it can be drawn on a jquery canvas"""
    # fixing body
    for x in data['you']['body']:
        x['x'] *= mod
        x['y'] *= mod

    # generating head
    data['you']['head'] = data['you']['body'][0]

    # for getting myself out of the enemies list
    snakes = []

    # fixing enemy bodies
    for y in data['board']['snakes']:
        # skipping self, we dont need to draw ourselves twice
        if y['name'] == data['you']['name']:
            continue

        # enlarging bodies
        for x in y['body']:
            x['x'] *= mod
            x['y'] *= mod

        # generating head
        y['head'] = y['body'][0]

        snakes.append(y)

    # I am not my own enemy.... or am I?
    data['board']['snakes'] = snakes

    # expanding board size
    data['board']['width'] *= mod
    data['board']['height'] *= mod

    # food
    for x in data['board']['food']:
        x['x'] *= mod
        x['y'] *= mod

    return data

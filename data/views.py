from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import controller as c
from .models import Game
import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GameView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # parsing data
            data = json.loads(request.body)

            # getting gid, if not in request it will raise a key error
            # and we will tell the client they dun goofed
            gid = data['gid']

            # getting game from gid, we dont use this variable,
            # we just want to ensure the game exists. If it doesnt this
            # function will raise an index error
            game = c.get_game_by_gid(gid)
        except KeyError:
            return HttpResponse(status=404, content=json.dumps({
                'error': 'invalid request'
            }))
        except IndexError:
            return HttpResponse(status=404, content=json.dumps({
                'error': 'game not found'
            }))
        except json.decoder.JSONDecodeError:
            print('bad request: ', request, request.body)
            return HttpResponse(status=400, content=json.dumps({
                'error': 'bad request',
            }))

        try:
            data = json.dumps(c.package_game_for_watch(gid))
            print(data)
            return HttpResponse(status=200, content=data)
        except Exception:
            return HttpResponse(status=500, content=json.dumps({
                'error': 'internal error, probably multiple games with that GID'
            }))

    def post(self, request):
        """
            Post takes the following options:
            option:
                - start
                - end
                - turn
            data
                - game data
        """
        try:
            # loading request
            r = json.loads(request.body)

            # very simple data validation
            option = r['option']
            data = r['data']

            # verifying option is either start/end/turn
            if option != 'start' and option != 'end' and option != 'turn':
                raise BadRequest

            # raises BadRequest exception
            simple_validate_game_data(r['data'])

            # all checks passed. We are pretty sure the data is valid at this point
            if option == 'start':
                c.create_game(data)
            if option == 'turn':
                c.save_turn(data)
            if option == 'end':
                c.end_game(data)

            return HttpResponse(status=200)

        except json.decoder.JSONDecodeError:
            print('bad request: ', request, request.body)
            return HttpResponse(status=400, content=json.dumps({
                'error': 'bad request',
            }))
        except BadRequest:
            return HttpResponse(status=404, content=json.dumps({
                'error': 'invalid request'
            }))
        except KeyError:
            return HttpResponse(status=404, content=json.dumps({
                'error': 'invalid request json'
            }))

    def delete(self, request):
        try:
            r = json.loads(request.body)
            gid = r['gid']

            if 'turn' in r:
                # we need to delete  the specified turn
                c.delete_turn(gid, r['turn'])
            else:
                # deleting whole game because turn was not specified
                c.delete_game(gid)

            return HttpResponse(status=200)

        except json.decoder.JSONDecodeError:
            print('bad request: ', request, request.body)
            return HttpResponse(status=400, content=json.dumps({
                'error': 'bad request',
            }))


@csrf_exempt
def list_game(request):
    gameList = []

    for game in Game.objects.all():
        gameList.append(str(game))

    response = json.dumps({"games": gameList})
    return HttpResponse(status=200, content=response)


def simple_validate_game_data(data):
    try:
        d = data['game']['id']
    except KeyError:
        raise BadRequest("game id")
    try:
        d = data['turn']
    except KeyError:
        raise BadRequest("turn")
    try:
        d = data['board']
    except KeyError:
        raise BadRequest("board")
    try:
        d = data['you']
    except KeyError:
        raise BadRequest("you")


class BadRequest(Exception):
    pass
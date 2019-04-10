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

    def post(self, request):
        """
            Adds a single turn to the database, to the appropriate game

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
        """
        This view just deletes a specified GID or Turn

        To delete a whole game:
            {
                'gid': <gid requested>
            }
        To delete a turn:
            {
                'gid': <gid requested>,
                'turn': <turn number to delete>
            }
        """
        try:
            r = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            print("bad json:" + str(request.body))
            return HttpResponse(status=400, content=json.dumps({
                'error': 'bad request',
            }))

        gid = r['gid']

        if 'turn' in r:
            # we need to delete  the specified turn
            c.delete_turn(gid, r['turn'])
        else:
            # deleting whole game because turn was not specified
            c.delete_game(gid)

        return HttpResponse(status=200)

    def get(self, request):
        """
        This view just returns a specified GID
        It does not require any authentication to access.

        Request must have:
            {
                'gid': <gid requested>
            }
        """
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


@csrf_exempt
def list_game(request):
    """
    This view just returns the list of all of the GIDs in the database
    It does not require any authentication to access.
    """
    gameList = []

    for game in Game.objects.all():
        gameList.append(str(game))

    response = json.dumps({"games": gameList})
    return HttpResponse(status=200, content=response)


@csrf_exempt
def get_game(request):
    """
    This view just returns a specified GID
    It does not require any authentication to access.

    Request must have:
        {
            'gid': <gid requested>
        }
    """
    if request.method != 'POST':
        return HttpResponse(status=404, content=json.dumps({
            'error': 'invalid method, requires POST'
        }))
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

class CallSnakeView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
            MUST BE AUTHENTICATED!

            The plan is the webpage will recieve the URL of the snake
            from the user, and the user will specify which turn they want
            to have the snake compute a move for

            Then the webpage will call this view.

            This views function is to call battlesnakes.

            Parameters
            {
                'URL':'http://localhost/',
                'data': {Turn object}
            }

            This function performs simple validation on the data
        """
        try:
            # loading request
            return HttpResponse(status=200)
        except Exception:
            return HttpResponse(status=404, content=json.dumps({
                'error': 'invalid request'
            }))
        except KeyError:
            return HttpResponse(status=404, content=json.dumps({
                'error': 'invalid request json'
            }))


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
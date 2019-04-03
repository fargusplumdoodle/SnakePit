import requests
from .models import Game, Turn
import time
from django.utils import timezone
import json
from ithiessen.settings import DATA_HOST


def send_data(option, data):
    content = json.dumps({
        'option': option,
        'data': data
    })
    r = requests.post(url=DATA_HOST + "/games", data=content, auth=('fargusD', '1234asdf'))
    if r.status_code != 200:
        raise ValueError('Host returned a non 200 status code: ' + r.status_code)


def delete_turn(gid, turn_no):
    # deletes all turns with the specified turn and game
    game = Game.objects.get(gid=gid)
    Turn.objects.filter(game=game, turnNo=turn_no).delete()


def create_game(data):
    '''
    This function creates and saves a game in the database with the specified name
    :param data: game id
    '''
    gid = data['game']['id']
    snake_name = data['you']['name']

    newGame = Game(gid=gid, snake_name=snake_name, width=data['board']['width'], height=data['board']['height'] )
    newGame.save()

    print('Created new game:', gid, 'snake:', snake_name)


def save_turn(data):
    game = get_game(data)

    # creating new turn object
    turn = Turn(turnNo=data['turn'], game=game, data=json.dumps(data))

    # saving turn to database
    turn.save()


def end_game(data):
    # getting game object
    game = get_game(data)

    # noting the time that the game ended
    game.time_ended = timezone.now()

    # saving last turn
    save_turn(data)

    # saving to database
    game.save()


def delete_game(gid):
    # deleting all games with specified GID
    Game.objects.filter(gid=gid).delete()


def play_one_frame(gid=None, turn=2):
    # frame=3 is ab
    if gid is None:
        gid = load_recent_gid()
    else:
        gid = gid

    # getting game object
    game = Game.objects.get(gid=gid)

    # gettting specific turn
    turn = Turn.objects.get(game=game, turnNo=turn)

    # leading json from turn
    data = json.loads(turn.data)

    game = Game.Game(data)

    # Computing move
    move = game.main()

    # TESTING
    #clear_board(game)
    #game.board.negative_manip_weight_around_point((4,4), -50, 4)
    #game.board.manip_weight_around_point((4,4), -50, 4)

    # printing off board
    game.board.print_board()

    # Generating info bar
    move = 'Move: ' + move
    turn = 'Turn: ' + str(game.data['turn'])

    # this is to ensure the gid remains centered
    space = ' ' * int((64 - len(move) - len(turn) - len(gid)) / 2)

    # printing info bar
    print(move + space + gid + space + turn)


def play_game(gid=None, speed=1):
    # example gid: af4ef54f-3842-476b-80a7-4455934ed2fc

    if gid is None:
        gid = load_recent_gid()
    else:
        gid = gid

    # very much assuming the game exists
    game = Game.objects.get(gid=gid)

    for turn in Turn.objects.filter(game=game):
        # creating game for this turn
        turnGame = Game.Game(json.loads(turn.data))

        # calculating move (and what the board looks like)
        move = turnGame.main()

        # clearing screen
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

        # Generating info bars
        food_weight = turnGame.foodWeight
        move = 'Move: ' + move
        turn = 'Turn: ' + str(turnGame.data['turn'])
        # this is to ensure the gid remains centered
        space = ' ' * int((64 - len(move) - len(turn) - len(gid)) / 2)

        print('Food Weight: ', food_weight, '    Health: ', turnGame.me.health)

        # printing off board
        turnGame.board.print_board()



        # printing info bar
        print(move + space + gid + space + turn)

        # sleeping for a second
        time.sleep(speed)
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')


def get_game(data):
    """
    Loads the game object from
    :param data: json request from battlesnake gmae
    :return: game object from database
    """
    gid = data['game']['id']

    # getting game object
    return Game.objects.filter(gid=gid)[0]


def get_game_by_gid(gid):
    """
    Loads the game object from
    :param data: json request from battlesnake gmae
    :return: game object from database
    """
    # getting game object
    return Game.objects.filter(gid=gid)[0]


def load_recent_gid():
    # returns the most recently played game
    return Game.objects.all().order_by('-id')[0].gid


def clear_board(game):
    for x in game.board.weightBoard:
        game.board.weightBoard[x] = 0
    # erasing snakes
    game.board.game.me.body = []
    game.board.game.enemy_bodies = []
    game.board.game.food = []


def get_frame(gid=None, turn=2):
    """
    gets frame as string
    for use in webpages
    :param gid:  gid of game
    :param turn:  turn of game
    :return: string
    """

    return_str = ''
    # frame=2 is ab
    if gid is None:
        gid = load_recent_gid()
    else:
        gid = gid

    # getting game object
    game = Game.objects.get(gid=gid)

    # gettting specific turn
    turn = Turn.objects.get(game=game, turnNo=turn)

    # leading json from turn
    data = json.loads(turn.data)

    game = Game.Game(data)

    # Computing move
    move = game.main()

    # TESTING
    #clear_board(game)
    #game.board.negative_manip_weight_around_point((4,4), -50, 4)
    #game.board.manip_weight_around_point((4,4), -50, 4)

    # printing off board
    return_str += game.board.get_board() + '\n'

    # Generating info bar
    move = 'Move: ' + move
    turn = 'Turn: ' + str(game.data['turn'])

    # this is to ensure the gid remains centered
    space = ' ' * int((64 - len(move) - len(turn) - len(gid)) / 2)

    # printing info bar
    return_str += move + space + gid + space + turn + '\n'
    return return_str


def package_game_for_watch(gid=None):
    # example gid: af4ef54f-3842-476b-80a7-4455934ed2fc
    """
    This function puts all turns into a single json object from the database

    if gid is provided it will load the most recent game

    :param gid: the gid of the game you want to watch
    :return: a dictionary including all turns
    """

    if gid is None:
        gid = load_recent_gid()
    else:
        gid = gid

    # very much assuming the game exists
    game = Game.objects.get(gid=gid)

    # return object, this will be a list of all turns
    returnGame = {
        'width': None,
        'height': None,
        'gid': gid,
        'turn': []
    }

    # adding turns to game
    for turn in Turn.objects.filter(game=game):
        # creating game for this turn
        turnData = json.loads(turn.data)

        # adding turn to game
        returnGame['turn'].append(turnData)

    # adding width / height to game
    print(returnGame['turn'][0]['board']['width'])

    return returnGame



import requests
from .models import Game, Turn
import time
from django.utils import timezone
import json
from ithiessen.settings import DATA_HOST


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
    :param data: game object
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

    game_queryset = Game.objects.filter(gid=gid)

    if len(game_queryset) == 0:
        raise ValueError('Requested game does not exist in database')

    return game_queryset.first()


def get_game_by_gid(gid):
    """
    Loads the game object from
    :param data: json request from battlesnake gmae
    :return: game object from database
    """
    game_queryset = Game.objects.filter(gid=gid)

    if len(game_queryset) == 0:
        raise ValueError('Requested game does not exist in database')

    return game_queryset.first()


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



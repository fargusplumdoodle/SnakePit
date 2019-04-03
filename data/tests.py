# from django.test import TestCase
import random
import requests
import json

DATA_HOST = 'http://localhost:8000'

game = {
    "you": {
        "health": 98,
        "body": [
            {
                "y": 3,
                "x": 14
            },
            {
                "y": 4,
                "x": 14
            },
            {
                "y": 4,
                "x": 13
            }
        ],
        "name": "SekhnetSnek",
        "id": "13e7d710-dfb9-45c2-919d-5dacbf609686"
    },
    "turn": 0,
    "board": {
        "snakes": [
            {
                "health": 98,
                "body": [
                    {
                        "y": 4,
                        "x": 11
                    },
                    {
                        "y": 3,
                        "x": 11
                    },
                    {
                        "y": 3,
                        "x": 12
                    }
                ],
                "name": "Son of Robosnake",
                "id": "213cd80c-ef75-404c-968b-db2733ac6fbe"
            },
            {
                "health": 98,
                "body": [
                    {
                        "y": 3,
                        "x": 14
                    },
                    {
                        "y": 4,
                        "x": 14
                    },
                    {
                        "y": 4,
                        "x": 13
                    }
                ],
                "name": "SekhnetSnek",
                "id": "13e7d710-dfb9-45c2-919d-5dacbf609686"
            }
        ],
        "width": 17,
        "height": 10,
        "food": [
            {
                "y": 4,
                "x": 16
            },
            {
                "y": 0,
                "x": 5
            },
            {
                "y": 7,
                "x": 8
            },
            {
                "y": 0,
                "x": 0
            },
            {
                "y": 0,
                "x": 7
            },
            {
                "y": 4,
                "x": 1
            },
            {
                "y": 1,
                "x": 5
            },
            {
                "y": 1,
                "x": 12
            },
            {
                "y": 9,
                "x": 4
            },
            {
                "y": 9,
                "x": 5
            }
        ]
    },
    "game": {
        "id": "NewTestGame1"
    }
}

game['game']['id'] = 't_' + str(random.choice(range(40)))


def api_test():
    def send_data(option, data):
        content = json.dumps({
            'option': option,
            'data': data
        })
        r = requests.post(url=DATA_HOST + "/games/", data=content, auth=('fargusD', '1234asdf'))
        if r.status_code != 200:
            raise ValueError('Host returned a non 200 status code: ' + str(r.status_code))

    # start testing
    send_data('start', game)

    # sending turns
    for i in range(3):
        game['turn'] += 1
        send_data('turn', game)

    # ending game
    game['turn'] += 1
    send_data('end', game)

# r = requests.delete(url=DATA_HOST + "/games", data=json.dumps({'gid': game['game']['id']}), auth=('fargusD', '1234asdf'))
# if r.status_code != 200:
#     raise ValueError('Host returned a non 200 status code: ' + r.status_code)
#
# def snake_test():
#
#     def send_data(option, data):
#         content = json.dumps(data)
#         r = requests.post(url=DATA_HOST + "/SekhnetSnake/" + option, data=content)
#         if r.status_code != 200:
#             raise ValueError('Host returned a non 200 status code: ' + r.status_code)
#         print(r.content.decode('utf-8'))
#
#     # start testing
#     send_data('start', game)
#
#     # sending turns
#     for i in range(3):
#         game['turn'] += 1
#         send_data('move', game)
#
#     # ending game
#     game['turn'] += 1
#     send_data('end', game)
#
#     # r = requests.delete(url=DATA_HOST + "/games", data=json.dumps({'gid': game['game']['id']}), auth=('fargusD', '1234asdf'))
#     # if r.status_code != 200:
#     #     raise ValueError('Host returned a non 200 status code: ' + r.status_code)
#     # print(r.content)

if __name__ == '__main__':
    api_test()
# snake_test()


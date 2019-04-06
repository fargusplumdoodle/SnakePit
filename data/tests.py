from django.test import TestCase
import random
import requests
import json

DATA_HOST = 'http://localhost:8000'


class APITest(TestCase):
    def setUp(self):
        # declaring sample game from template
        self.game = {
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

        # generating simple random gid
        self.game['game']['id'] = 't_' + str(random.choice(range(40)))
        print(self.game['game']['id'])

    @staticmethod
    def send_data(option, data):
        # this sends data to the game endpoint
        # option is what stage of the game it is
        # start, turn, end
        content = json.dumps({
            'option': option,
            'data': data
        })
        r = requests.post(url=DATA_HOST + "/games/", data=content, auth=('fargusD', '1234asdf'))
        if r.status_code != 200:
            raise ValueError('Host returned a non 200 status code: ' + str(r.status_code))

    def test_send_battlesnake_game_to_games_endpoint(self):
        # start testing
        self.send_data('start', self.game)

        # sending turns
        for i in range(3):
             self.game['turn'] += 1
             self.send_data('turn', self.game)

        # ending game
        self.game['turn'] += 1
        self.send_data('end', self.game)




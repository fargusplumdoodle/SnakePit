# from django.test import TestCase
from unittest import TestCase
from django.contrib.auth.models import User
from data.models import Game, Turn
import random
import requests
import json


'''
Assertions trigger when the statement is FALSE... you fool
'''


class TestGameEndpoint(TestCase):
    def setUp(self):
        # setting up game info
        self.DATA_HOST = 'http://localhost:8000'
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
        self.gid = 't_' + str(random.choice(range(40)))
        self.game['game']['id'] = self.gid

        # setting up user info
        self.username = 'fargusD'
        self.password = '1234asdf'

    def send_data(self, option, data):
        content = json.dumps({
            'option': option,
            'data': data
        })
        r = requests.post(url=self.DATA_HOST + "/games/", data=content, auth=(self.username, self.password))
        return r

    def create_game(self, gid):
        # creating new gid for this game
        previous_gid = self.game['game']['id']
        self.gid = gid
        self.game['game']['id'] = gid

        # --- set up ----
        self.send_data('start', self.game)

        # sending turns
        for i in range(3):
            self.game['turn'] += 1
            self.send_data('turn', self.game)

        # ending game
        self.game['turn'] += 1
        self.send_data('end', self.game)

        # cleaning up
        self.gid = previous_gid
        self.game['game']['id'] = previous_gid

    def test_create_game_properly(self):
        # --- set up ----
        self.send_data('start', self.game)

        # sending turns
        for i in range(3):
            self.game['turn'] += 1
            self.send_data('turn', self.game)

        # ending game
        self.game['turn'] += 1
        self.send_data('end', self.game)

        # --- asserting the funnel cakes ----
        game = Game.objects.filter(gid=self.gid).first()

        assert game is not None  # Checking if game was created
        assert game.width == self.game['board']['width']
        assert game.height == self.game['board']['height']

    def test_delete_endpoint(self):
        # ---- creating temp game
        gid = 'temp_12345'
        self.create_game(gid)

        # ---- test deleting turns
        game = Game.objects.get(gid=gid)
        num_turns = len(Turn.objects.filter(game=game))

        for x in range(num_turns):
            content = json.dumps({
                'gid': gid,
                'turn': x + 1
            })
            r = requests.delete(url=self.DATA_HOST + "/games/", data=content, auth=(self.username, self.password))
            assert r.status_code == 200

        assert len(Turn.objects.filter(game=game)) == 0  # should be no remaining games

        # ---- test deleting game
        content = json.dumps({
            'gid': gid
        })
        r = requests.delete(url=self.DATA_HOST + "/games/", data=content, auth=(self.username, self.password))

        assert r.status_code == 200  # status code should be 200 when we delete the game we just made

    def test_send_turns_to_a_nonexistent_game(self):
        # --- set up ----
        # self.send_data('start', self.game)

        # making invalid gid
        self.game['game']['id'] = self.gid + 'asdf'

        # sending turns
        for i in range(3):
            self.game['turn'] += 1
            r = self.send_data('turn', self.game)
            assert r.status_code == 404  # status code should be 404

        # ending game
        self.game['turn'] += 1
        r = self.send_data('end', self.game)
        assert r.status_code == 404  # status code shouldn't be 200 after we sent invalid data

    def tearDown(self):
        Game.objects.filter(gid='temp_12345').delete()

        # deleting test game object
        if len(Game.objects.filter(gid=self.gid)) > 0:
            Game.objects.filter(gid=self.gid).delete()



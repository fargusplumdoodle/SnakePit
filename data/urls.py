"""
DATA ENDPOINT!

############## GAME ENDPOINT #################
POST <SnakePitURL>/game
{
    "gid": "testGame1"
}

Response:
The response will contain all turns for the specified game
If the game does not exist in the database, it will return a 404 error

############## GAME LIST ENDPOINT #################
POST <SnakePitURL>/game/list

Response:
response will be a list of all games in the database
{
    "games": ["game1", "game2"...]
}

look ma I can document
"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url('list', views.list_game),
    url('', views.GameView.as_view()),
]

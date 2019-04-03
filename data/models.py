from django.db import models


class Game(models.Model):
    gid = models.CharField(max_length=20)
    time_started = models.DateTimeField(auto_now_add=True)
    time_ended = models.DateTimeField(null=True)
    width = models.IntegerField(default=7)
    height = models.IntegerField(default=7)
    snake_name = models.CharField(max_length=21, null=True)
    def __str__(self):
        return self.gid


class Turn(models.Model):
    turnNo = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
        return self.game.gid + '_' + str(self.turnNo)



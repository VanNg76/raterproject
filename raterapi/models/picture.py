from django.db import models

from .player import Player
from .game import Game

class Picture(models.Model):

    link = models.CharField(max_length=100)
    caption = models.CharField(max_length=50)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

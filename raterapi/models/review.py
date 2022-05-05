from django.db import models

from .player import Player
from .game import Game

class Review(models.Model):

    review = models.CharField(max_length=100)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

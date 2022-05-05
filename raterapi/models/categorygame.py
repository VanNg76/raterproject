from django.db import models

from .category import Category
from .game import Game

class CategoryGame(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

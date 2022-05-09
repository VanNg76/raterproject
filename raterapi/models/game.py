from django.db import models

# from .player import Player


class Game(models.Model):

    title = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    designer = models.CharField(max_length=20)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    estimate_time_to_play = models.IntegerField()
    age_recommendation = models.IntegerField()
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    categories = models.ManyToManyField("Category")

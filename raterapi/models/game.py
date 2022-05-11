from django.db import models

from raterapi.models.rate import Rate

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

    @property
    def is_creator(self):
        return self.__is_creator

    @is_creator.setter
    def is_creator(self, value):
        self.__is_creator = value

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rate.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rate

        # Calculate the average and return it.
        if len(ratings) == 0:
            return 0
        else:
            return total_rating / len(ratings)

class GamePicture(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name='pictures')
    game_image = models.ImageField(
        upload_to='gamepictures', height_field=None,
        width_field=None, max_length=None, null=True)

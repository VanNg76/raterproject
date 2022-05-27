"""Module for generating games report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterreports.views.helpers import dict_fetch_one


class ReviewGame(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to the most review game
            db_cursor.execute("""
                SELECT GameId, GameTitle, MAX(number_of_reviews) as no_reviews
                FROM (
                SELECT g.id GameId, g.title GameTitle, COUNT(g.id) AS number_of_reviews
                FROM raterapi_game g
                JOIN raterapi_review re
                    ON re.game_id = g.id
                GROUP BY g.id
                )
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            data = dict_fetch_one(db_cursor)
        
        # The template string must match the file name of the html template
        template = 'games/themostreview.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "gamebyreview": data
        }

        return render(request, template, context)

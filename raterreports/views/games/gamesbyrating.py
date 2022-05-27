"""Module for generating games report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterreports.views.helpers import dict_fetch_all


class GameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games and ratings
            db_cursor.execute("""
                SELECT g.id, g.title, avg(ra.rate) AS average_rate
                FROM raterapi_rate ra
                JOIN raterapi_game g
                    ON ra.game_id = g.id
                GROUP BY g.id
                ORDER BY average_rate DESC
                LIMIT 3
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
        
        # The template string must match the file name of the html template
        template = 'games/gamesbyrating.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "gamesbyrating_list": dataset
        }

        return render(request, template, context)

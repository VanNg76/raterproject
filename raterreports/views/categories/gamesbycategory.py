"""Module for generating games by category report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterreports.views.helpers import dict_fetch_all


class CategoryGameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games by category
            db_cursor.execute("""
                SELECT c.label Category, g.id GameId, g.title GameTitle
                FROM raterapi_game g
                JOIN raterapi_game_categories gc
                    ON gc.game_id = g.id
                JOIN raterapi_category c
                    ON c.id = gc.category_id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each category.
            # This will be the structure of the games_by_category list:
            #
            # [
            #   {
            #     "id": 1,
            #     "category": "Dice",
            #     "games": [
            #       {
            #         "id": 1,
            #         "title": "Foo"
            #       },
            #       {
            #         "id": 2,
            #         "title": "Foo 2"
            #       }
            #     ]
            #   },
            # ]

            games_by_category = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the id, title from the row dictionary
                game = {
                    'id': row['GameId'],
                    'title': row['GameTitle']
                }
                
                # This is using a generator comprehension to find the category_dict in the games_by_category list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # category_dict = None
                # for category_game in games_by_category:
                #     if category_game['category'] == row['category']:
                #         category_dict = category_game
                
                category_dict = next(
                    (
                        category_game for category_game in games_by_category
                        if category_game['category'] == row['Category']
                    ),
                    None
                )
                
                if category_dict:
                    # If the category_dict is already in the games_by_category list, append the game to the games list
                    category_dict['games'].append(game)
                else:
                    # If the user is not on the games_by_category list, create and add the user to the list
                    games_by_category.append({
                        "category": row['Category'],
                        "games": [game]
                    })
        
        # The template string must match the file name of the html template
        template = 'categories/gamesbycategory.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "categorygame_list": games_by_category
        }

        return render(request, template, context)

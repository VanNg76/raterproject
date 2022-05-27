from urllib import request
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterapi.models import Game, Player
from raterapi.views.game import GameSerializer, CreateGameSerializer

class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'players', 'categories', 'games', 'rates', 'reviews']
    
    def setUp(self):
        # Grab the first Player object from the database and add their token to the headers
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_game(self):
        """Create game test"""
        url = "/games"

        # Define the Game properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        game = {
            "title": "Test Game",
            "description": "Test description",
            "designer": "Milton Bradley",
            "year_released": 1999,
            "number_of_players": 6,
            "age_recommendation": 15,
            "estimate_time_to_play": 20
        }

        response = self.client.post(url, game, format='json')

        # The _expected_ output should come first when using an assertion with 2 arguments
        # The _actual_ output will be the second argument
        # We _expect_ the status to be status.HTTP_201_CREATED and it _actually_ was response.status_code
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        # Get the last game added to the database, it should be the one just created
        new_game = Game.objects.last()

        # Since the create method should return the serialized version of the newly created game,
        # Use the serializer you're using in the create method to serialize the "new_game"
        # Depending on your code this might be different
        expected = CreateGameSerializer(new_game)

        # Now we can test that the expected ouput matches what was actually returned
        self.assertEqual(expected.data, response.data)


    def test_get_game(self):
        """Get Game Test  """
        # Grab a game object from the database
        game = Game.objects.first()

        url = f'/games/{game.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Ad is_creator and run the game through the serializer
        # that's being used in view
        if game.player_id == self.player.id:
            game.is_creator = True
        else:
            game.is_creator = False

        expected = GameSerializer(game)
        
        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)


    def test_list_games(self):
        """Test list games"""
        url = '/games'

        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        # Get all the games in the database and serialize them to get the expected output
        all_games = Game.objects.all()
        for game in all_games:
            if game.player_id == self.player.id:
                game.is_creator = True
            else:
                game.is_creator = False
        expected = GameSerializer(all_games, many=True)
        
        self.assertEqual(expected.data, response.data)


    def test_change_game(self):
        """test update game"""
        # Grab the first game in the database
        game = Game.objects.first()
        
        url = f'/games/{game.id}'

        updated_game = {
            "title": f'{game.title} up',
            "description": game.description,
            "designer": game.designer,
            "year_released": game.year_released,
            "number_of_players": game.number_of_players,
            "age_recommendation": game.age_recommendation,
            "estimate_time_to_play": game.estimate_time_to_play
        }

        response = self.client.put(url, updated_game, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Refresh the game object to reflect any changes in the database
        game.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_game['title'], game.title)


    def test_delete_game(self):
        """Test delete game"""
        game = Game.objects.first()

        url = f'/games/{game.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Test that it was deleted by trying to _get_ the game
        # The response should return a 404
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
from urllib import request
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterapi.models import Rate, Player
from raterapi.views.rate import CreateRateSerializer

class RateTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'players', 'games', 'rates']
    
    def setUp(self):
        # Grab the first Player object from the database
        # and add their token to the headers
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_rate(self):
        """Create rate test"""
        url = "/rates"

        # Define the Rate properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        rate = {
            "rate": 9,
            "game": 1,
            "player": 1
        }

        response = self.client.post(url, rate, format='json')

        # The _expected_ output should come first when using an assertion with 2 arguments
        # The _actual_ output will be the second argument
        # We _expect_ the status to be status.HTTP_201_CREATED and it _actually_ was response.status_code
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        # Get the last game added to the database, it should be the one just created
        new_rate = Rate.objects.last()

        # Since the create method should return the serialized version of the newly created game,
        # Use the serializer you're using in the create method to serialize the "new_game"
        # Depending on your code this might be different
        expected = CreateRateSerializer(new_rate)

        # Now we can test that the expected ouput matches what was actually returned
        self.assertEqual(expected.data, response.data)

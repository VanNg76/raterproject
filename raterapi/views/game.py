"""View module for handling requests about game types"""
# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action

# use in create to validate receiving errors
# from django.core.exceptions import ValidationError

from raterapi.models import Player
from raterapi.models import Game

class GameView(ViewSet):
    """Rater game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game
        """
        try:
            game = Game.objects.get(pk=pk)
            if game.player_id == request.auth.user.id:
                game.is_creator = True
            else:
                game.is_creator = False
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game
        Returns:
            Response -- JSON serialized list of game
        """
        games = Game.objects.all()
        
        for game in games:
            if game.player_id == request.auth.user.id:
                game.is_creator = True
            else:
                game.is_creator = False

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized game instance
        """

        player = Player.objects.get(user=request.auth.user) # a player is not returned from client, it is added here in server

        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(player=player)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        """(is working!! update function without validation)
        Handle PUT requests for a game"""

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.number_of_players = request.data["number_of_players"]
        game.age_recommendation = request.data["age_recommendation"]
        game.estimate_time_to_play = request.data["estimate_time_to_play"]
        game.year_released = request.data["year_released"]
        
        player = Player.objects.get(user=request.auth.user)
        game.player = player
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # def update(self, request, pk):
    #     """Handle PUT requests for a game
    #     update function with validation
    #     """
    #     game = Game.objects.get(pk=pk)
    #     game_type = GameType.objects.get(pk=request.data['game_type'])
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     # The original game object is passed to the serializer, along with the request.data
    #     # This will make any updates on the game object
    #     serializer = CreateGameSerializer(game, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(game_type=game_type, gamer=gamer)
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk):
    #     game = Game.objects.get(pk=pk)
    #     game.delete()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        # Using depth to embed tables: fields need to revise to
        # 'game_type''gamer' instead of 'game_type_id''gamer_id'
        fields = ('id', 'title', 'description', 'designer', 'number_of_players',
                  'is_creator', 'year_released', 'age_recommendation', 'player_id',
                  'estimate_time_to_play', 'categories', 'average_rating')
        depth = 1

class CreateGameSerializer(serializers.ModelSerializer):
    """use for create (validation received data from client)"""
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'number_of_players', 'year_released', 'age_recommendation', 'estimate_time_to_play')

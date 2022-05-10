"""View module for handling requests about game types"""
# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from raterapi.models import Player
from raterapi.models import Game
from raterapi.models import Rate

class RateView(ViewSet):
    """Rater rate view"""

    # def retrieve(self, request, pk):
    #     """Handle GET requests for single rate
    #     Returns:
    #         Response -- JSON serialized rate
    #     """
    #     try:
    #         rate = Review.objects.get(pk=pk)
    #         serializer = RatingSerializer(rate)
    #         return Response(serializer.data)
    #     except Review.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # def list(self, request):
    #     """Handle GET requests to get all rate
    #     Returns:
    #         Response -- JSON serialized list of rate
    #     """
    #     reviews = Review.objects.all()
    #     game = request.query_params.get('game', None)
    #     player = Player.objects.get(user=request.auth.user)
        
    #     if game is not None:
    #         rates = rates.filter(game_id=game)
    #         rates = rates.filter(player_id=player)
        
    #     serializer = RatingSerializer(rates, many=True)
    #     return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized rate instance
        """

        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game'])
        
        serializer = CreateRateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(player=player, game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class RateSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Rate
        fields = ('id', 'rate', 'player', 'game')
        depth = 1

class CreateRateSerializer(serializers.ModelSerializer):
    """use for create (validation received data from client)"""
    class Meta:
        model = Rate
        fields = ('id', 'rate', 'game')

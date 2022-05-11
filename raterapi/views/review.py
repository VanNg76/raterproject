"""View module for handling requests about game types"""
# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from raterapi.models import Player
from raterapi.models import Game
from raterapi.models import Review

class ReviewView(ViewSet):
    """Rater review view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single review
        Returns:
            Response -- JSON serialized review
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all review
        Returns:
            Response -- JSON serialized list of review
        """
        reviews = Review.objects.all()
        game = request.query_params.get('game', None)
        # player = Player.objects.get(user=request.auth.user)
        
        if game is not None:
            reviews = reviews.filter(game_id=game)
            # reviews = reviews.filter(player_id=player)
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized review instance
        """

        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game'])
        
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(player=player, game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Review
        fields = ('id', 'review', 'player', 'game')
        depth = 1

class CreateReviewSerializer(serializers.ModelSerializer):
    """use for create (validation received data from client)"""
    class Meta:
        model = Review
        fields = ('id', 'review', 'game')

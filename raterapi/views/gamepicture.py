from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.files.base import ContentFile
import base64, uuid

from raterapi.models import GamePicture, Game

class GamePictureView(ViewSet):
    """Rater game picture view"""

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized game picture instance
        """
        
        # Create a new instance of the game picture model you defined
        game_picture = GamePicture()
        game = Game.objects.get(pk=request.data['game'])
        game_picture.game = game
        format, imgstr = request.data["game_image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["game"]}-{uuid.uuid4()}.{ext}')

        # Give the image property of your game picture instance a value
        # For example, if you named your property `game_image`, then
        # you would specify the following code:
        game_picture.game_image = data

        serializer = CreateGamePictureSerializer(data=game_picture.__dict__)
        serializer.is_valid(raise_exception=True)
        game_picture.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CreateGamePictureSerializer(serializers.ModelSerializer):
    """use for create (validation received data from client)"""
    class Meta:
        model = GamePicture
        fields = ('id', 'game_image', 'game_id')
 

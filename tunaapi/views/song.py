from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist

class SongView(ViewSet):
    """Level up song view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song

        Returns:
            Response -- JSON serialized song
        """
        song = Song.objects.get(pk=pk)
        serializer = SongSerializer(song, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        """Handle GET requests to get all song

        Returns:
            Response -- JSON serialized list of song
        """
        song = Song.objects.all()
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all song

        Returns:
            Response -- JSON serialized list of song
        """
        song = Song.objects.all()
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
        """Handle POST operations

        Returns
          Response -- JSON serialized song instance
        """
        
        artist = Artist.objects.get(id=request.data["artist_id"])
        
        song = Song.objects.create(
            title=request.data["title"],
            artist=artist,
            album=request.data["album"],
            length=request.data["length"],
        )
        serializer = SongSerializer(song, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a song

        Returns:
          Response -- Empty body with 204 status code
        """

        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = request.data["length"]
        artist = Artist.objects.get(pk=request.data["artist_id"])
        song.artist = artist

        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
    def destroy(self, response, pk):
        """Deletes Data

        Returns:
            Response: Empty body with 204 code
        """
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs
    """
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'length')
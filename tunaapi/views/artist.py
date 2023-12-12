from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song

class ArtistView(ViewSet):
    """Level up artist view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist

        Returns:
            Response -- JSON serialized artist
        """
        artist = Artist.objects.get(pk=pk)
        
        song = Song.objects.filter(artist=artist.id)
        artist.songs = song
        # songcount = artist.songs
        
        # songs = Artist.objects.annotate(song_count=Count(songcount))
        
        serializer = ArtistSerializer(artist, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        """Handle GET requests to get all artist

        Returns:
            Response -- JSON serialized list of artist
        """
        artist = Artist.objects.all()
        
        for a in artist:
            songs = Song.objects.filter(artist=a.id)
            a.songs = songs
        
        serializer = ArtistSerializer(artist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
        """Handle POST operations

        Returns
          Response -- JSON serialized artist instance
        """
        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )
        serializer = ArtistSerializer(artist, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a artist

        Returns:
          Response -- Empty body with 204 status code
        """

        artist = Artist.objects.get(pk=pk)
      
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio= request.data["bio"]

        artist.save()
        
        serializer = ArtistSerializer(artist, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, response, pk):
        """Deletes Data

        Returns:
            Response: Empty body with 204 code
        """
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs
    """
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'length' )
class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists

    """
    songs = SongSerializer(many=True, read_only=True)
    songs_count = serializers.SerializerMethodField(default=None)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'songs_count', 'songs')
    def get_songs_count(self, obj):
        return obj.songs.count()
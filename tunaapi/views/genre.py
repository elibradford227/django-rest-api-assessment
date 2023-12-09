from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre

class GenreView(ViewSet):
    """Level up genre view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single genre

        Returns:
            Response -- JSON serialized genre
        """
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        """Handle GET requests to get all genre

        Returns:
            Response -- JSON serialized list of genre
        """
        genre = Genre.objects.all()
        serializer = GenreSerializer(genre, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
        """Handle POST operations

        Returns
          Response -- JSON serialized genre instance
        """
        genre = Genre.objects.create(
            description=request.data["description"],
        )
        serializer = GenreSerializer(genre, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a genre

        Returns:
          Response -- Empty body with 204 status code
        """

        genre = Genre.objects.get(pk=pk)
      
        genre.description = request.data["description"]

        genre.save()
        
        serializer = GenreSerializer(genre, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, response, pk):
        """Deletes Data

        Returns:
            Response: Empty body with 204 code
        """
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
      
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genres
    """
    class Meta:
        model = Genre
        fields = ('id', 'description' )
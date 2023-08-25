from listening_to.api.spotify import Spotify
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def currently_playing_song(request):
    return Response(Spotify().currently_playing())
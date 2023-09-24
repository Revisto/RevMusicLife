from django.http import HttpResponse
from django.template import loader
from django.template.response import TemplateResponse
import requests

def listening_to(request):
    template = loader.get_template('listening_to.html')
    return HttpResponse(template.render())

def top_tracks(request):
    top_tracks_response = requests.get('http://localhost:8000/api/top-tracks/')
    if top_tracks_response.status_code == 200:
        top_tracks_data = top_tracks_response.json()
    return TemplateResponse(request, 'top_tracks.html', {'top_tracks': top_tracks_data})
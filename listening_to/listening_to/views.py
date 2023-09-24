from django.http import HttpResponse
from django.template import loader

def listening_to(request):
    template = loader.get_template('listening_to.html')
    return HttpResponse(template.render())
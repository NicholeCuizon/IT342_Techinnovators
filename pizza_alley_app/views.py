from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

from pizza_alley_app.models import CurrentOrder, Products

# Create your views here.
def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())
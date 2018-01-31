from django.shortcuts import render
from .models import Rooms

# Create your views here.

def index(request):
    rooms = Rooms.objects.order_by('pk')
    context = {'rooms' : rooms}
    return render(request, 'my/index.html', context)

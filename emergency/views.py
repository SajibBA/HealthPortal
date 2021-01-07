from django.shortcuts import render

# Create your views here.


def emergency(request):
    return render(request, 'emergency/emergency.html')
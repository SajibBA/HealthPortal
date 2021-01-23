from django.shortcuts import render


# Emergency page redirect


def emergency(request):
    return render(request, 'emergency/emergency.html')
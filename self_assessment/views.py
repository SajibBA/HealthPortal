from django.shortcuts import render

# Create your views here.

def self_assessment(request):
    return render(request, 'self_assessment/self_assessment.html')
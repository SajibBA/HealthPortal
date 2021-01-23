from django.shortcuts import render

# Redirect to self assessment

def self_assessment(request):
    return render(request, 'self_assessment/self_assessment.html')
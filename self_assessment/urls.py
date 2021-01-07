from django.urls import path

from . import views

urlpatterns = [
    path('self_assessment/',
         views.self_assessment,
         name='self_assessment')

]
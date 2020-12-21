
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', Login.as_view(), name='login'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/normal/', NormalSignUpView.as_view(), name='normal_signup'),
    path('accounts/signup/professional/', ProfessionalSignUpView.as_view(), name='professional_signup'),
    path(r'edit_profile/normal', NormalProfileEditView.as_view(), name='normal_edit_profile'),
    path(r'edit_profile/professional/', ProfessionalProfileEditView.as_view(), name='professional_edit_profile'),
    path(r'profile/', views.profile, name='profile'),
    path(r'profile_home/', views.profile_home, name='profile_home'),
    path(r'change_password/', ProfilePasswordChangeView.as_view(), name='change_password'),
    path(r'view_professionals/', views.view_professionals, name='view_professionals'),
    path(r'search_professionals/', views.search_professionals, name='search_professionals'),
    path(r'view_professionals_profile/(?P<pk>\d+)/', views.view_professionals_profile, name='view_professionals_profile'),
    path(r'send_message/(?P<pk>\d+)/', views.send_message, name='send_message'),
    path(r'view_messages/', views.view_messages, name='view_messages'),
    path(r'update_message/(?P<pk>\d+)/', views.update_message, name='update_message'),
    path(r'delete_message/(?P<pk>\d+)/', views.delete_message, name='delete_message'),

]


from .views import *
from django.urls import path, include
from .views import Authenticated,ResultExplorer


urlpatterns = [
    path('register/', Signup.as_view(), name='register'),
    path(r'upload/', Authenticated.as_view(), name='file-upload'),
    path(r'filter/', Authenticated.as_view(), name='filter'),
    path(r'delete/', Authenticated.as_view(), name='delete-entries'),
    path(r'explorer/', ResultExplorer.as_view(), name='display'),]
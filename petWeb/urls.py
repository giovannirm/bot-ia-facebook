from django.urls import path

from petWeb.controllers.veterinarycontroller import login

urlpatterns = [
    path('login/', login),
]
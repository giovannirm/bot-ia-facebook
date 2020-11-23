from django.urls import path
from petWeb.views import login, home

urlpatterns = [
    #path('login/', login , name = "login"),
    path('home/', home, name = "home"),
    path('login/', login, name = "login"),
]


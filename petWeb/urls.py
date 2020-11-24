from django.urls import path
from petWeb.views import *

urlpatterns = [
    path('home/', home, name = "home"),
    path('login/', login, name = "login"),
    path('add_disease/', add_disease, name = "add"),
    path('update_disease/', update_disease, name = "update"),
    path('delete_disease/', delete_disease, name = "delete"),
    path('read_diseases/', read_diseases, name = "read"),    
]



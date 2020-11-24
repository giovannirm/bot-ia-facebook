from django.urls import path
from petWeb.views import *

urlpatterns = [
    path('home/', home, name = "home"),
    path('', login, name = "login"),
    path('add_disease/', add_disease, name = "add"),
    path('update_disease/<int:id>', update_disease, name = "update"),
    path('delete_disease/<int:id>', delete_disease, name = "delete"),
    path('read_diseases/', read_diseases, name = "read"),    
]



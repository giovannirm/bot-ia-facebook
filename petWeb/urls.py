from django.urls import path
from petWeb.views import *

urlpatterns = [
    path('home/', home, name = "home"),
    path('', login, name = "login"),
    path('webhook/', webhook, name = "webhook"),
    path('add_disease/', add_disease, name = "add"),
    path('update_disease/', update_disease, name = "update"),
    path('delete_disease/<int:id>', delete_disease, name = "delete"),
    path('read_diseases/', read_diseases, name = "read"),    
    path('modal_update/<int:id>', modal_update, name = "modal_update"),    
    path('modal_read/<int:id>', modal_read, name = "modal_read"),    
]



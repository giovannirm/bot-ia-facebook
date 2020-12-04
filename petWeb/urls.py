from django.urls import path, re_path
#from django.conf.urls import include, url
from .views import *

urlpatterns = [       
    path('home/', home, name = "home"),
    path('', login, name = "login"),    
    path('add_disease/', add_disease, name = "add"),
    path('update_disease/', update_disease, name = "update"),
    path('delete_disease/<int:id>', delete_disease, name = "delete"),
    path('read_diseases/', read_diseases, name = "read"),    
    path('modal_update/<int:id>', modal_update, name = "modal_update"),    
    path('modal_read/<int:id>', modal_read, name = "modal_read"),    
    re_path(r'^b55b2d9ad2d0a9108960aca01097ef20efd403a5b552a08787/?$', Webhook.as_view(), name = "webhook"),
]
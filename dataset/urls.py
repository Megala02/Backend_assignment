from django.urls import path
from . import views
urlpatterns = [
    #for creating a key value pair
    path('create',views.create),
    #for reading a key value pair
    path('read',views.read),
    #for reading all key value pair
    path('readAll',views.readAll),
    #for deleting a key value pair
    path('delete',views.delete),
]

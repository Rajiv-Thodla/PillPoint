from django.urls import path
from . import views

urlpatterns = [

    path("<int:id>" , views.function1 , name = "function1"),

]
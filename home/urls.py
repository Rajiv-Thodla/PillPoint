from django.urls import path
from .views import home  # Import the home function

urlpatterns = [
    path('', home, name='home'),  # This sets the home page URL
]

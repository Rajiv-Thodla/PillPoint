from django.urls import path
from .views import home,contact,about  # Import the home function

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
]

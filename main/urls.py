from django.urls import path
from . import views

urlpatterns = [
    path("function1/<int:id>/", views.function1, name="function1"),  # Prefixed path
]

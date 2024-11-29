from . import views
from django.urls import path, include



urlpatterns = [
    path('',  views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
]

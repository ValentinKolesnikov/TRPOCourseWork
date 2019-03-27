from django.urls import path, include
from . import views


urlpatterns = [
    path('<int:id>', views.restaurant, name='restaurant_with_id'),
    path('like/<int:id>', views.like, name='restaurant_with_id', ),
    path('create/', views.create),
]
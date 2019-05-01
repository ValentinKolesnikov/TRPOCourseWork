from django.urls import path, include
from . import views


urlpatterns = [
    path('<int:id>', views.restaurant, name='restaurant_with_id'),
    path('like', views.like,),
    path('create/', views.create),
    path('editor/', views.editor),
    path('tables/', views.editortables),
]
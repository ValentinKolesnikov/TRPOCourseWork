from django.urls import path, include
from . import views


urlpatterns = [
    path('<int:id>', views.user, name='user_with_id'),
    path('editor/', views.editor)
]
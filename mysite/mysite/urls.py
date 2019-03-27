from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('user/', include('user.urls')),
    path('auth/', include('loginsystem.urls')),
    path('', include('mainApp.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
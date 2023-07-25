from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('PemoranchApp.urls')),
    path('', include('pemoranchees.urls')),
]

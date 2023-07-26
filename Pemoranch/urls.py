from django.contrib import admin
from django.urls import path, include

from pemoranchees import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('PemoranchApp.urls')),
    path('', include('pemoranchees.urls')),
    path('pemos/', views.pemoran_list_view),
    path('pemos/<int:pemoran_id>', views.pemoran_details_view, name='pemoran_details_view'),
]

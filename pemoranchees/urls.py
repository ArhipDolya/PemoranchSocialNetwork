from django.urls import path
from . import views


urlpatterns = [
    path('pemoranchees/<int:pemoran_id>', views.pemoran_details_view, name='pemoran_details_view'),
]

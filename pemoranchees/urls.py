from django.urls import path
from . import views


urlpatterns = [
    path('', views.pemoran_list_view),
    path('<int:pemoran_id>/', views.pemoran_details_view, name='pemoran_details_view'),
    path('create-pemoran/', views.pemoran_create_view, name='pemoran_create_view'),
    path('<int:pemoran_id>/delete/', views.pemoran_delete_view, name='pemoran_delete_view'),
    path('action/', views.pemoran_action_view, name='pemoran_action_view'),
    
]


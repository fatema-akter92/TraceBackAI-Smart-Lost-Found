from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('map/', views.map_view, name='map_view'),
    path('location/', views.map_view, name='location_view'),
    path('locations/', views.map_view, name='locations_view'),
    path('analytics/', views.analytics_view, name='analytics_view'),
    path('about/', views.about_view, name='about_view'),
]

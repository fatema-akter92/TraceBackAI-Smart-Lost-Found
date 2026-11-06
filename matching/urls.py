from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('matches/<int:match_id>/<str:action>/', views.handle_match_action, name='handle_match_action'),
]

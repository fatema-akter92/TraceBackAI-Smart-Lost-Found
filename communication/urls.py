from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('start/<int:item_id>/', views.start_thread, name='start_thread'),
    path('<int:thread_id>/', views.thread_detail, name='thread_detail'),
]

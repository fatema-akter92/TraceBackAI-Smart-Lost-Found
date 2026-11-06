from django.urls import path
from . import views

urlpatterns = [
    path('desks/', views.desk_list, name='desk_list'),
    path('desk/<int:desk_id>/', views.desk_detail, name='desk_detail'),
    path('deposit/<int:item_id>/', views.deposit_item, name='deposit_item'),
    path('scanner/', views.qr_scanner, name='qr_scanner'),
    path('verify/<str:tracking_code>/', views.verify_item_qr, name='verify_item_qr'),
    path('handover/<int:custody_id>/', views.execute_handover, name='execute_handover'),
    path('receipt/<int:custody_id>/', views.handover_receipt, name='handover_receipt'),
]

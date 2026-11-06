from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('report/lost/', views.report_lost, name='report_lost'),
    path('report/found/', views.report_found, name='report_found'),
    path('<int:item_id>/', views.item_detail, name='item_detail'),
    path('<int:item_id>/claim/', views.submit_claim, name='submit_claim'),
    path('<int:item_id>/matches/', views.item_matches, name='item_matches'),
    path('<int:item_id>/status/<str:new_status>/', views.update_item_status, name='update_item_status'),
    path('claim/<int:claim_id>/<str:action>/', views.review_claim, name='review_claim'),
    path('complaint/', views.file_complaint, name='file_complaint'),
    path('fraud-center/', views.admin_fraud_review, name='admin_fraud_review'),
    path('api/ai-category-suggest/', views.ai_category_suggest, name='ai_category_suggest'),
]

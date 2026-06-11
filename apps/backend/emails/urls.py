from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('process_emails/', views.process_emails_view, name='process_emails'),
    path('update_email/<str:email_id>/', views.update_email, name='update_email'),
    path('config/', views.config_view, name='config_view'),
]

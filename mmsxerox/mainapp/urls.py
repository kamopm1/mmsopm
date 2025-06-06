from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send-contact-otp/', views.send_contact_otp, name='send_contact_otp'),
    path('send-email-otp/', views.send_email_otp, name='send_email_otp'),
]

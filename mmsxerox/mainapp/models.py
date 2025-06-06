# mainapp/models.py
from django.db import models

class CustomerSupport(models.Model):
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)  # <-- Make sure this exists
    contact_otp = models.CharField(max_length=6)
    place = models.CharField(max_length=100)
    email = models.EmailField()
    email_otp = models.CharField(max_length=6)
    suggestions = models.TextField()

    def __str__(self):
        return self.name

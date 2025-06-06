from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# For demo, store OTPs in memory (NOT for production)
# In production, store in DB or cache with expiry

contact_otp_storage = {}
email_otp_storage = {}

def index(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        contact = request.POST.get('contact', '').strip()
        place = request.POST.get('place', '').strip()
        email = request.POST.get('email', '').strip()
        suggestions = request.POST.get('suggestions', '').strip()
        contact_otp = request.POST.get('contactOtp', '').strip()
        email_otp = request.POST.get('emailOtp', '').strip()

        # Validate required fields
        if not (name and contact and place and email):
            context['error'] = "Please fill in all required fields."
            return render(request, 'mainapp/index.html', context)

        # Validate contact OTP
        stored_contact_otp = contact_otp_storage.get(contact)
        if not stored_contact_otp or stored_contact_otp != contact_otp:
            context['error'] = "Invalid or missing Contact OTP."
            return render(request, 'mainapp/index.html', context)

        # Validate email OTP
        stored_email_otp = email_otp_storage.get(email)
        if not stored_email_otp or stored_email_otp != email_otp:
            context['error'] = "Invalid or missing Email OTP."
            return render(request, 'mainapp/index.html', context)

        # If all valid, clear stored OTPs (one-time use)
        contact_otp_storage.pop(contact, None)
        email_otp_storage.pop(email, None)

        # You can save the data to DB here or send email, etc.
        context['success'] = "Thank you for your feedback!"

        # Optionally clear form or do other logic
        return render(request, 'mainapp/index.html', context)

    return render(request, 'mainapp/index.html', context)


from django.http import JsonResponse
import random

def send_contact_otp(request):
    if request.method == "POST":
        contact = request.POST.get('contact', '').strip()
        if len(contact) == 10 and contact.isdigit():
            otp = str(random.randint(100000, 999999))
            contact_otp_storage[contact] = otp
            # Here, you would send OTP via SMS gateway instead of print
            print(f"Contact OTP for {contact}: {otp}")
            return JsonResponse({'success': True, 'message': 'OTP sent to contact number.'})
        return JsonResponse({'success': False, 'message': 'Invalid contact number.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def send_email_otp(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        if email:
            otp = str(random.randint(100000, 999999))
            email_otp_storage[email] = otp
            # Here, send email OTP via email backend instead of print
            print(f"Email OTP for {email}: {otp}")
            return JsonResponse({'success': True, 'message': 'OTP sent to email.'})
        return JsonResponse({'success': False, 'message': 'Invalid email.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

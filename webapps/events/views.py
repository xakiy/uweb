import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reservation, EventPage
# from .services import TelegramService, WhatsAppService # Custom service classes
from .models import Reservation


class TelegramService:
    def send_verification_link(self, phone_number, verification_code, reservation_id):
        # Replace with your bot token
        token = "YOUR_TELEGRAM_BOT_TOKEN"
        # Telegram requires username or chat_id, not phone number directly
        # This assumes the user has added the bot as a contact
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": phone_number, # Or user_id
            "text": f"🎟️ Event Reservation Code: {verification_code}\nID: {reservation_id}"
        }
        requests.post(url, data=data)


class WhatsAppService:
    def send_verification_link(self, phone_number, verification_code, reservation_id):
        # Requires Twilio Account SID and Auth Token
        url = "https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        params = {
            "From": "+1234567890",
            "To": phone_number,
            "Body": f"Your Event Verification Code is {verification_code}"
        }
        # Use requests.post(url, params=params)
        pass


def request_reservation(request):
    if request.method == 'POST':
        # 1. Validate Event
        event_page = request.POST.get('event_id')
        event = EventPage.objects.get(id=event_page)

        if event.max_attendees <= event.reservations.count():
            return render(request, 'error.html', {'error': 'Event is full.'})

        # 2. Create or get anonymous user
        session_id = request.session.session_key
        anonymous_user, created = AnonymousUser.objects.get_or_create(
            email=request.POST.get('email'),
            defaults={
                'full_name': request.POST.get('full_name'),
                'phone_number': request.POST.get('phone_number'),
                'session_id': session_id
            }
        )

        # 3. Create Reservation
        reservation = Reservation.objects.create(
            event=event,
            anonymous_user=anonymous_user,
            status='pending'
        )

        # 4. Generate Verification Code
        code = reservation.verification_code

        # 5. Send via Telegram/WhatsApp
        if request.POST.get('platform') == 'whatsapp':
            WhatsAppService().send_verification_link(
                reservation.phone_number, code, reservation.id
            )
        else:
            TelegramService().send_verification_link(
                reservation.phone_number, code, reservation.id
            )

        return render(request, 'events/success.html', {'message': 'Verification code sent to your phone.'})

    return render(request, 'events/reservation_form.html')


def verify_identity(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        reservation = Reservation.objects.filter(verification_code=code).first()

        if reservation and reservation.status == 'pending':
            reservation.status = 'verified'
            reservation.save()
            return redirect('reservation_success', reservation_id=reservation.id)
        return render(request, 'error.html', {'error': 'Invalid or Expired Code'})

    return render(request, 'events/verify_identity.html')


def reservation_success(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)

    # Send confirmation email
    send_mail(
        subject=f'Reservation Confirmed - {reservation.event.event_title}',
        message=f'''
        Dear {reservation.full_name},

        Your reservation has been successfully confirmed!

        Event: {reservation.event.event_title}
        Date: {reservation.event.start_time.strftime('%Y-%m-%d %H:%M')}
        Duration: {reservation.event.duration_minutes} minutes

        Reservation ID: {reservation.id}

        Thank you for attending!
        ''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reservation.email],
        fail_silently=False,
    )

    return render(request, 'events/reservation_success.html', {'reservation': reservation})

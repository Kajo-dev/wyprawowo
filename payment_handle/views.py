from django.shortcuts import render, redirect
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import time
from .models import UserPayment
from user_manager.models import User
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):
    if request.method == 'POST':
        YOUR_DOMAIN = settings.SITE_URL
        user = request.user
        UserPayment.objects.create(user=user).save()
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'blik', 'p24', 'paypal'],
            line_items=[
                {
                    'price_data': {
                        'currency': "PLN",
                        'unit_amount': 500,
                        'product_data': {
                            'name': "Opłata aktywacyjna konta",
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=YOUR_DOMAIN + 'payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + 'payment/cancel/',
        )
        return redirect(checkout_session.url, code=303)


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.id
    user_payment = UserPayment.objects.get(user=user_id)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    return render(request, 'payment_handle/success.html', {'customer': customer})


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return render(request, 'payment_handle/cancel.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_success = True
        user_payment.save()
    return HttpResponse(status=200)
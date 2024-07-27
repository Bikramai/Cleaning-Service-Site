import stripe
from django.contrib import messages
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from root.settings import BASE_URL, STRIPE_SECRET_KEY
from src.services.payments.notify import notify_admin_and_user_on_service_create
from src.services.services.models import ServiceRequest


@csrf_exempt
def create_checkout_session(request, pk):

    obj = get_object_or_404(ServiceRequest, pk=pk)
    stripe.api_key = STRIPE_SECRET_KEY

    # Create a Price object in Stripe
    price = stripe.Price.create(
        unit_amount=int(obj.service.price * 100),  # Price in cents
        currency='usd',
        product_data={
            'name': obj.service.name,
        },
    )

    session = stripe.checkout.Session.create(
        line_items=[{
            'price': price.id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payments:success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payments:cancelled')) + "?session_id={CHECKOUT_SESSION_ID}"
    )

    obj.checkout_id = session.id
    obj.save()

    return redirect(session.url, code=303)


class SuccessView(TemplateView):
    template_name = 'payments/success.html'

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            raise Http404

        try:
            stripe.api_key = STRIPE_SECRET_KEY
            session = stripe.checkout.Session.retrieve(session_id)
        except Exception as e:
            raise Http404

        obj = get_object_or_404(ServiceRequest, checkout_id=session_id)

        if obj.is_paid:
            raise Http404

        messages.success(request, 'Payment successful')
        obj.is_paid = True
        obj.save()

        notify_admin_and_user_on_service_create(obj)

        return render(request, self.template_name)


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')

        if session_id is None:
            raise Http404

        obj = get_object_or_404(ServiceRequest, checkout_id=session_id)

        if obj.is_paid:
            raise Http404

        obj.delete()

        messages.error(request, 'Payment cancelled and your request deleted')
        return render(request, self.template_name)



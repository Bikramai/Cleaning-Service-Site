from django.urls import path

from .views import (
    SuccessView, CancelledView, create_checkout_session
)


app_name = 'payments'
urlpatterns = [
    path('create-checkout-session/<int:pk>/', create_checkout_session, name='create-checkout-session'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancelled/', CancelledView.as_view(), name='cancelled'),
]

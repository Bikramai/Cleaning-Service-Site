from django.urls import path

from .views import (
    HomeView, ServicesView, TermsView,
    ContactView, ContactCreateView,
    ServicesDetailView
)

app_name = "website"
urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    # path('booking/', BookingView.as_view(), name='booking'),
    path('services/', ServicesView.as_view(), name='services'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('contact/create/', ContactCreateView.as_view(), name='contact-create'),
    path('service/detail/<int:pk>', ServicesDetailView.as_view(), name='services_detail'),

]

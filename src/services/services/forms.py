from django.forms import ModelForm

from .models import ServiceRequest


class ServicesRequestForm(ModelForm):

    class Meta:
        model = ServiceRequest
        fields = ['name', 'email', 'phone', 'address', 'city', 'country', 'service', 'message']

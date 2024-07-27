from django.core.exceptions import ValidationError
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=2, unique=True, help_text='ISO 3166-1 alpha-2')
    language = models.CharField(max_length=10, default='en', help_text='ISO 639-1', null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD', help_text='ISO 4217', null=True, blank=True)
    phone_code = models.CharField(max_length=4, default='+1', help_text='e.g. +1', null=True, blank=True)

    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

    def clean(self):
        if self.country.is_available is False:
            raise ValidationError('Services are not available in this country')
        return super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
        return super().delete(*args, **kwargs)

    @property
    def services_available(self):
        return self.country.is_available


class Application(models.Model):
    name = models.CharField(max_length=100, help_text='Application name', default='AGS LTD')
    short_name = models.CharField(max_length=10, help_text='Your application short name', default='AGS')
    tagline = models.CharField(
        max_length=100, help_text='Your application business line', default='Reliable Services, Remarkable Results.'
    )
    description = models.TextField(
        default="Reliable Services, Remarkable Results.",
        help_text='Application description'
    )

    favicon = models.ImageField(
        upload_to='core/application/logos', null=True, blank=True, help_text='Application favicon'
    )
    logo = models.ImageField(
        upload_to='core/application/logos', null=True, blank=True,
        help_text='Application real colors logo'
    )
    logo_dark = models.ImageField(
        upload_to='core/application/logos', null=True, blank=True, help_text='For dark theme only'
    )
    logo_light = models.ImageField(
        upload_to='core/application/logos', null=True, blank=True, help_text='For light theme only'
    )

    contact_email1 = models.EmailField(
        max_length=100, default='ags_ltd@gmail.com', help_text='Application contact email 1'
    )
    contact_email2 = models.EmailField(
        max_length=100, default='ags_ltd@gmail.com', help_text='Application contact email 2'
    )
    admin_email = models.EmailField(
        default="admin_ags_ltd@gmail.com",
        help_text="Whenever a service request arrives admin will be notified using this email"
    )
    contact_phone1 = PhoneNumberField(
        help_text='Application contact phone 1', default='+12125552368'
    )
    contact_phone2 = PhoneNumberField(
        help_text='Application contact phone 2', default='+12125552368'
    )

    address = models.CharField(
        max_length=255, help_text='office address', default='Near Natural History Museum London UK'
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=6, help_text='latitude', default=51.5011785334205)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, help_text='longitude', default=-0.17576576072915845)

    terms_url = models.URLField(
        max_length=255, default='https://ags-ltd.com/terms-of-use/', help_text='Terms and Conditions page link'
    )

    version = models.CharField(max_length=10, help_text='Current version', default='1.0.0')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Application"
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        if Application.objects.count() > 1:
            raise ValidationError('You are not allowed to add more than one record')
        return super().clean()


class NewsLetter(models.Model):
    email = models.EmailField(max_length=100, unique=True)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['email']
        verbose_name_plural = "Newsletters"

    def __str__(self):
        return self.email


class Contact(models.Model):
    name = models.CharField(max_length=75, help_text="Your Name")
    email = models.EmailField(max_length=100)
    phone_number = PhoneNumberField(
        help_text='Application contact phone 2', default='+923259575875'
    )
    message = models.TextField(max_length=255)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
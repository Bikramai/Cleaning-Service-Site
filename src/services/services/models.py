from django.core.exceptions import ValidationError
from django.db import models
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
from django_ckeditor_5.fields import CKEditor5Field

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('completed', 'Completed'),
    ('in_progress', 'In Progress'),
)


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to="core/service-categories/images", null=True, blank=True,
        help_text='Service Category Image must be PNG [500*500]'
    )

    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    content = CKEditor5Field('content', config_name='extends', null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = ResizedImageField(
        null=True, blank=True, size=[500, 500], quality=75, force_format='PNG',
        upload_to='core/services/images', help_text='Service Image must be PNG [500*500]'
    )
    
    background_image =  ResizedImageField(
        null=True, blank=True, size=[1024, 720], quality=75, force_format='PNG',
        upload_to='core/services/images', help_text='Background Image must be PNG [1024*720]'
    )

    is_available = models.BooleanField(default=True, help_text='Is this service available to use')

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['-created_on']
        get_latest_by = 'created_on'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete(save=True)
        super(Service, self).delete(*args, **kwargs)
    
    


class ServiceRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField()
    address = models.CharField(max_length=255)
    country = models.ForeignKey('core.Country', on_delete=models.CASCADE)
    city = models.ForeignKey('core.City', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField()

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    checkout_id = models.CharField(max_length=1000, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'
        ordering = ['-created_on']
        get_latest_by = 'created_on'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.amount = self.service.price
        return super().save(force_insert, force_update, using, update_fields)

    def clean(self):
        if not self.service.is_available:
            raise ValidationError('This Service is not available')

        if not self.city.country.is_available:
            raise ValidationError(f"Services aren't available for {self.city.country.name}")

        return super().clean()

import folium
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from src.core.bll import get_or_create_application
from src.core.forms import ContactForm
from src.core.models import NewsLetter
from src.services.services.models import Service
from django.views.generic import DetailView


class HomeView(TemplateView):
    template_name = "website/index.html"


class ContactView(TemplateView):
    template_name = "website/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app = get_or_create_application()
        markers = folium.Map(location=[app.latitude, app.longitude], zoom_start=6)
        co_ordinates = (app.latitude, app.longitude)
        folium.Marker(co_ordinates, popup=str(app.name)).add_to(markers)
        context['map'] = markers._repr_html_()

        return context


class ServicesView(TemplateView):
    template_name = "website/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Service.objects.all()
        return context


class TermsView(TemplateView):
    template_name = "website/terms.html"


""" EXTERNAL APPS """


class NewsLetterSubscribeView(View):

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Please provide an email')
            return redirect(request.META.get('HTTP_REFERER'))

        emails = NewsLetter.objects.filter(email=email)
        if emails:
            messages.error(
                request, 'You have already subscribed to our newsletter')
            return redirect(request.META.get('HTTP_REFERER'))

        NewsLetter.objects.create(email=email)
        messages.success(
            request, 'You have successfully subscribed to our newsletter')
        return redirect(request.META.get('HTTP_REFERER'))


class ContactCreateView(View):
    template_name = "website/contact.html"

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been submitted successfully")
            return redirect("website:contact")
        else:
            messages.error(request, "Something is wrong with your request please check your form")

        return render(request, self.template_name, {"form": form})


class ServicesDetailView(DetailView):
    template_name = "website/services_detail.html"
    model = Service

    def get_context_data(self, **kwargs):
        context = super(ServicesDetailView, self).get_context_data(**kwargs)
        context['other_services'] = Service.objects.all()[:8]
        
        return context
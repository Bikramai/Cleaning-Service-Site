from random import choice

from django.db import IntegrityError
from django.utils import timezone
from faker import Faker

from src.core.models import Country, City, NewsLetter, Contact
from src.services.accounts.models import User
from src.services.services.models import Service, ServiceCategory, ServiceRequest


fake = Faker()


""" HELPERS """


def __print_start(model):
    print()
    print(f"__ BUILD: {model} START __")


def __print_ended(model):
    print(f"__ BUILD: {model} ENDED __")
    print()


""" GLOBALS """


def country_fake():
    __print_start("Country")
    countries = [
        {
            "name": "United Kingdom",
            "short_name": "UK",
            "language_code": "en_UK",
            "currency_code": "GBP",
            "phone_code": "+44"
        },
    ]

    for country in countries:
        name = country['name']
        short_name = country['short_name']
        language = country['language_code']
        currency = country['currency_code']
        phone_code = country['phone_code']

        try:
            Country.objects.create(
                name=name, short_name=short_name, language=language, currency=currency,
                phone_code=phone_code
            )

            print(f"---- object: {country['name']} faked.")
        except IntegrityError as e:
            print(e.__str__())

    __print_ended("Country")


def city_fake():
    # add some of the main cities of the UK
    __print_start("City")
    cities = [
        {
            "name": "London",
        },
        {
            "name": "Manchester",
        },
        {
            "name": "Birmingham",
        },
        {
            "name": "Liverpool",
        },
        {
            "name": "Glasgow",
        },
        {
            "name": "Bristol",
        },
        {
            "name": "Leeds",
        },
        {
            "name": "Sheffield",
        },
        {
            "name": "Edinburgh",
        },
        {
            "name": "Cardiff",
        },
    ]
    for city in cities:
        name = city['name']
        country = Country.objects.first()

        try:
            City.objects.create(
                name=name, country=country
            )

            print(f"---- object: {city['name']} faked.")
        except IntegrityError as e:
            print(e.__str__())

    __print_ended("City")


def news_letter_fake():
    __print_start("NewsLetter")
    for _ in range(10):
        email = fake.email()
        try:
            NewsLetter.objects.create(email=email)
            print(f"---- object: {email} faked.")
        except IntegrityError as e:
            print(e.__str__())
    __print_ended("NewsLetter")


def contact_fake():
    __print_start("Contact")
    for _ in range(10):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        message = fake.text()
        try:
            Contact.objects.create(name=name, email=email, phone_number=phone, message=message)
            print(f"---- object: {name} faked.")
        except IntegrityError as e:
            print(e.__str__())
    __print_ended("Contact")


""" ACCOUNTS FAKER """


def user_fake(total=10):
    __print_start("User")

    for count in range(total):
        profile = fake.simple_profile()
        user = User.objects.create_user(
            username=profile['username'],
            email=profile['mail'],
            password=fake.isbn13()
        )
        user.first_name = fake.first_name()
        user.last_name = fake.last_name()
        user.phone_number = fake.msisdn()
        user.save()

        print(f"---- object: {count} faked.")

    __print_ended("User")


""" SERVICES """
"""

1. Pressure Washing - Driveways, Patios, Decking and Bins
2. General Waste Removal
3. Basic Ground Works
4. Fascia’s and Gutter Cleaning
5. Domestic and Commercial  Cleaning - Basic - Intermediate - Deep Cleaning 
6. Oven Cleaning 
7. Clothes Ironing Services
8. Garden Maintenance Services
9. Handy Man Services 
10. Flat Roofing
11. Bespoke Summer Houses
12. Sheds
13. Fences
14. Property Management
15. Air B&B
"""


def service_categories_fake():
    categories = [
        "Cleaning Services",
        "Waste Management Services",
        "Ground Works Services",
        "Maintenance Services",
        "Roofing Services",
        "Construction Services",
        "Property Services"
    ]
    __print_start("Service Categories")
    for category in categories:
        try:
            ServiceCategory.objects.create(name=category)
            print(f"---- Category: {category} added.")
        except IntegrityError as e:
            print(e.__str__())
    __print_ended("Service Categories")


def services_fake():
    services = [
        {"name": "Pressure Washing - Driveways, Patios, Decking and Bins", "category_name": "Cleaning Services",
         "price": 50.00,
         "description": "Professional pressure washing service for driveways, patios, decking, and bins."},
        {"name": "General Waste Removal", "category_name": "Waste Management Services", "price": 100.00,
         "description": "Efficient removal of general waste and rubbish."},
        {"name": "Basic Ground Works", "category_name": "Ground Works Services", "price": 200.00,
         "description": "Basic ground works including leveling and preparation for construction projects."},
        {"name": "Fascia’s and Gutter Cleaning", "category_name": "Cleaning Services", "price": 80.00,
         "description": "Thorough cleaning of fascias and gutters to maintain their appearance and functionality."},
        {"name": "Domestic and Commercial Cleaning - Basic - Intermediate - Deep Cleaning",
         "category_name": "Cleaning Services", "price": 120.00,
         "description": "Comprehensive cleaning services ranging from basic to deep cleaning for both residential and commercial properties."},
        {"name": "Oven Cleaning", "category_name": "Cleaning Services", "price": 70.00,
         "description": "Specialized cleaning service for ovens to remove grease and grime."},
        {"name": "Clothes Ironing Services", "category_name": "Cleaning Services", "price": 30.00,
         "description": "Professional ironing services for clothes."},
        {"name": "Garden Maintenance Services", "category_name": "Maintenance Services", "price": 150.00,
         "description": "Regular maintenance and upkeep of gardens, including lawn mowing and hedge trimming."},
        {"name": "Handy Man Services", "category_name": "Maintenance Services", "price": 180.00,
         "description": "Versatile handyman services for various repairs and installations."},
        {"name": "Flat Roofing", "category_name": "Roofing Services", "price": 500.00,
         "description": "Installation and repair of flat roofing systems."},
        {"name": "Bespoke Summer Houses", "category_name": "Construction Services", "price": 2000.00,
         "description": "Custom-built summer houses tailored to your specifications."},
        {"name": "Sheds", "category_name": "Construction Services", "price": 800.00,
         "description": "Construction and installation of sheds for storage purposes."},
        {"name": "Fences", "category_name": "Construction Services", "price": 300.00,
         "description": "Installation and repair of fences for property boundaries."},
        {"name": "Property Management", "category_name": "Property Services", "price": 250.00,
         "description": "Comprehensive property management services including maintenance and tenant management."},
        {"name": "Air B&B", "category_name": "Property Services", "price": 120.00,
         "description": "Management and maintenance services for Air B&B properties."},
    ]
    __print_start("Services")
    for service in services:
        category_name = service['category_name']
        category = ServiceCategory.objects.get(name=category_name)

        try:
            Service.objects.create(
                name=service['name'], category=category, price=service['price'], description=service['description']
            )
            print(f"---- Service: {service['name']} added.")
        except IntegrityError as e:
            print(e.__str__())
    __print_ended("Services")


def service_requests_fake(num_requests=10):
    countries = Country.objects.all()
    cities = City.objects.all()
    services = Service.objects.all()

    __print_start("Service Requests")
    for _ in range(num_requests):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        address = fake.address()
        country = choice(countries)
        city = choice(cities)
        service = choice(services)
        message = fake.text()

        amount = fake.random_int(min=50, max=500)
        is_paid = fake.boolean(chance_of_getting_true=50)
        checkout_id = fake.uuid4()

        status = choice(['pending', 'confirmed', 'completed', 'cancelled'])
        created_on = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone())

        try:
            ServiceRequest.objects.create(
                name=name, email=email, phone=phone, address=address,
                country=country, city=city, service=service, message=message,
                amount=amount, is_paid=is_paid, checkout_id=checkout_id,
                status=status, created_on=created_on
            )
            print(f"---- Service request by {name} created.")
        except Exception as e:
            print(f"Error creating service request: {e}")

    __print_ended("Service Requests")


""" ============================================================================================== """


def main():
    # country_fake()
    # city_fake()
    # news_letter_fake()
    # contact_fake()

    # user_fake()

    # service_categories_fake()
    # services_fake()
    service_requests_fake()


if __name__ == '__main__':
    main()

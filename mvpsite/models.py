import uuid
from random import random

from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings


# Create your models here.
def create_ref():
    return str(random.randint(1000000000, 9999999999))

countries = [];
with open("countries.txt") as cs:
    for line in cs.readlines():
        line = line.split("|")
        countries.append((line[1], line[0]))

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")


class Address(models.Model):
    address = models.CharField(verbose_name="Address: ")
    address_2 = models.CharField(verbose_name="Address Line 2: ")
    state = models.CharField(verbose_name="State/Province: ")
    country = models.CharField(choices=countries, max_length=2, verbose_name="Country: ")
    postal_code = models.CharField(verbose_name="Postal Code: ")


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, primary_key=True, editable=False)
    profile = models.ImageField(verbose_name="Profile Picture: ")
    name_f = models.CharField(verbose_name="First Name: ")
    name_m = models.CharField(max_length=1, verbose_name="Middle Initial: ")
    name_l = models.CharField(verbose_name="Last Name: ")
    role_choices = [(0, "Sender"), (1, "Courier")]
    role = models.SmallIntegerField(choices=role_choices, verbose_name="Role: ")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="Home Address: ")
    phone_number = models.CharField(validators=[phone_regex], verbose_name="Cell Phone Number: ")
    rating = models.FloatField(default=0)
    referer = models.CharField(max_length=10, verbose_name="Referal Code: ", blank=True, editable=False)
    referee = models.CharField(max_length=10, default=create_ref, editable=False)


class KYCAuth(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.PROTECT, primary_key=True)
    status_choices = [(0, "Pending"), (1, "Completed Successfully"), (2, "Failed"), (3, "Raised to Supervisor")]
    status = models.SmallIntegerField(choices=status_choices, default=0)
    f_lic = models.ImageField(verbose_name="Front of driver's licence: ", editable=False)
    b_lic = models.ImageField(verbose_name="Back of driver's licence: ", editable=False)
    mail_item = models.ImageField(verbose_name="Piece of mail with your name and address: ", editable=False);


class CourierAd(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False);
    courier = models.ForeignKey(Profile, on_delete=models.PROTECT, editable=False)

    package_units = models.SmallIntegerField(choices=[(0, "Imperial"), (1, "Metric")], verbose_name="System of units: ")
    package_weight = models.FloatField(verbose_name="Maximum weight: ")
    package_price_min = models.FloatField(verbose_name="Price (USD): ")
    # package_price_cur = models.CharField(max_length=3, verbose_name="3-digit currency code: ")

    dep_city = models.CharField(max_length=3, verbose_name="Departure airport (3-letter code): ")
    dep_country = models.CharField(choices=countries, max_length=2, verbose_name="Departure country: ")
    dep_date = models.DateField(verbose_name="Date of departure: ")

    dest_city = models.CharField(max_length=3, verbose_name="Destination airport (3-letter code): ")
    dest_country = models.CharField(choices=countries, max_length=2, verbose_name="Destination country: ")
    dest_date = models.DateField(verbose_name="Date of arrival: ")

    status_code = [(-1, "Cancelled"), (0, "Still accepting offers"), (1, "A deal is in progress"), (2, "A deal is completed"),
                   (3, "The courier has departed"), (4, "The courier has arrived")]
    status = models.SmallIntegerField(choices=status_code, default=0)


class PackageAd(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False);
    desc = models.TextField(verbose_name="Description - Include what's in the package (hazards, fragile items): ")

    package_units = models.SmallIntegerField(choices=[(0, "Imperial"), (1, "Metric")], verbose_name="System of units: ")
    package_type = models.SmallIntegerField(choices=[(0, "In luggage"), (1, "Separate bag"), (2, "Oversize")], verbose_name="Type of package: ")
    package_weight = models.FloatField(verbose_name="Approximate weight: ")
    package_length = models.FloatField(verbose_name="Length: ")
    package_width = models.FloatField(verbose_name="Width: ")
    package_depth = models.FloatField(verbose_name="Depth: ")
    package_image = models.ImageField(verbose_name="Photo of the package: ")
    package_price_max = models.FloatField(verbose_name="Price maximum (USD): ")
    # package_price_cur = models.CharField(max_length=3, verbose_name="3-digit currency code: ")

    transport_modes = [(0, "In Person"), (1, "Delivery Service")]

    sender_mode = models.SmallIntegerField(choices=transport_modes, verbose_name="Pickup mode: ")
    sender_address = models.ForeignKey(Address, on_delete=models.PROTECT,
                                       verbose_name="Pickup address OR delivery service address: ")
    sender = models.ForeignKey(Profile, on_delete=models.PROTECT, editable=False)

    receiver_mode = models.SmallIntegerField(choices=transport_modes, verbose_name="Drop-off mode: ")
    receiver_number = models.CharField(validators=[phone_regex], verbose_name="Receiver's phone number: ")
    receiver_address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="Receiver's address NOT delivery service address: ")

    status_code = [(-1, "Cancelled"), (0, "Still accepting offers"), (1, "A deal is in progress"), (2, "A deal is completed"),
                   (3, "The package has been dropped off"), (4, "The package is with the courier"),
                   (5, "The courier has delivered the package"), (6, "The package has been received")]
    status = models.SmallIntegerField(choices=status_code, default=0)
    courier = models.ForeignKey(CourierAd, on_delete=models.PROTECT, null=True)
import uuid
from random import randint

from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.contrib import admin


# Create your models here.
def create_ref():
	return str(randint(1000000000, 9999999999))

countries = [];
with open(settings.STATICFILES_DIRS[0] + "/mvp/countries.txt") as cs:
	for line in cs.readlines():
		line = line.strip().split("|")
		countries.append((line[1], line[0]))

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")


class Address(models.Model):
	address = models.CharField(max_length=32, verbose_name="Address: ")
	address_2 = models.CharField(max_length=32, verbose_name="Address Line 2: ", blank=True)
	state = models.CharField(max_length=32, verbose_name="State/Province: ")
	city = models.CharField(max_length=32, verbose_name="City: ")
	country = models.CharField(choices=countries, max_length=2, verbose_name="Country: ")
	postal_code = models.CharField(max_length=32, verbose_name="Postal Code: ")


class Profile(models.Model):
	id = models.UUIDField(default=uuid.uuid4, editable=False)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, primary_key=True)
	profile = models.ImageField(verbose_name="Profile Picture: ", blank=True)
	name_f = models.CharField(max_length=32, verbose_name="First Name: ")
	name_l = models.CharField(max_length=32, verbose_name="Last Name: ")
	role_choices = [(0, "Sender"), (1, "Courier")]
	role = models.SmallIntegerField(choices=role_choices, verbose_name="Role: ")
	address = models.ForeignKey(Address, related_name="%(class)s_address", on_delete=models.PROTECT, verbose_name="Home Address: ")
	phone_number = models.CharField(max_length=32, validators=[phone_regex], verbose_name="Cell Phone Number: ")
	rating = models.FloatField(default=5)
	num_of_ratings = models.IntegerField(default=0)
	referer = models.CharField(max_length=10, verbose_name="Referral Code: ", blank=True)
	referee = models.CharField(max_length=10, default=create_ref)


@admin.display(description="Full Name")
def get_full_name(obj):
	return "%s %s" % (obj.name_f.upper(), obj.name_l.upper())


@admin.display(description="Address")
def get_full_address(obj):
	return "%s %s; %s, %s, %s" % (obj.address.address, obj.address.city, obj.address.state, obj.address.country, obj.address.postal_code)


class ProfileAdmin(admin.ModelAdmin):
	list_display = (get_full_name, get_full_address)


class KYCAuth(models.Model):
	user = models.OneToOneField(Profile, on_delete=models.PROTECT, primary_key=True)
	status_code = [(0, "Pending"), (1, "Completed Successfully"), (2, "Failed"), (3, "Raised to Supervisor")]
	status = models.SmallIntegerField(choices=status_code, default=0)
	f_lic = models.ImageField(verbose_name="Front of driver's licence: ")
	b_lic = models.ImageField(verbose_name="Back of driver's licence: ")
	mail_item = models.ImageField(verbose_name="Piece of mail with your name and address: ");


@admin.display(description="Status", ordering="status")
def get_status(obj):
	for c in obj.status_code:
		if obj.status == c[0]:
			return c[1]


@admin.display(description="Full Name")
def get_kyc_full_name(obj):
	return "%s %s" % (obj.user.name_f.upper(), obj.user.name_l.upper())


class KYCAdmin(admin.ModelAdmin):
	list_display = (get_status, get_kyc_full_name)


class CourierAd(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False);
	courier = models.ForeignKey(Profile, related_name="%(class)s_courier", on_delete=models.PROTECT)

	# package_units = models.SmallIntegerField(choices=[(0, "Imperial"), (1, "Metric")], verbose_name="System of units: ")
	package_weight = models.FloatField(verbose_name="Maximum weight (lb): ")
	package_price_min = models.FloatField(verbose_name="Price (USD): ")
	# package_price_cur = models.CharField(max_length=3, verbose_name="3-digit currency code: ")

	dep_airport = models.CharField(max_length=3, verbose_name="Departure airport (3-letter code): ")
	dep_country = models.CharField(choices=countries, max_length=2, verbose_name="Departure country: ")
	dep_date = models.DateField(verbose_name="Date of departure: ")

	dest_airport = models.CharField(max_length=3, verbose_name="Destination airport (3-letter code): ")
	dest_country = models.CharField(choices=countries, max_length=2, verbose_name="Destination country: ")
	dest_date = models.DateField(verbose_name="Date of arrival: ")

	status_code = [(0, "Still accepting offers"), (1, "A deal is in progress"), (2, "A deal is completed"),
				   (3, "The courier has departed"), (4, "The courier has arrived"), (7, "Cancelled"), (8, "Rated"), (9, "Attached")]
	status = models.SmallIntegerField(choices=status_code, default=0)
	package = models.ForeignKey("PackageAd", related_name="%(class)s_package", on_delete=models.PROTECT, null=True, default=None)


@admin.display(description="Courier Full Name")
def get_courier_full_name(obj):
	return "%s %s" % (obj.courier.name_f.upper(), obj.courier.name_l.upper())


class CourierAdmin(admin.ModelAdmin):
	list_display = (get_courier_full_name, get_status)


class PackageAd(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False);
	desc = models.TextField(verbose_name="Description - Include what's in the package (hazards, fragile items): ")

	# package_units = models.SmallIntegerField(choices=[(0, "Imperial"), (1, "Metric")], verbose_name="System of units: ")
	package_type = models.SmallIntegerField(choices=[(0, "In luggage"), (1, "Separate bag"), (2, "Oversize")], verbose_name="Type of package: ")
	package_weight = models.FloatField(verbose_name="Approximate weight (lb): ")
	package_length = models.FloatField(verbose_name="Length (in): ")
	package_width = models.FloatField(verbose_name="Width (in): ")
	package_depth = models.FloatField(verbose_name="Depth (in): ")
	package_image = models.ImageField(verbose_name="Photo of the package: ")
	package_price_max = models.FloatField(verbose_name="Price maximum (USD): ")
	# package_price_cur = models.CharField(max_length=3, verbose_name="3-digit currency code: ")

	transport_modes = [(0, "In Person"), (1, "Delivery Service")]

	# sender_mode = models.SmallIntegerField(choices=transport_modes, verbose_name="Pickup mode: ")
	sender_address = models.ForeignKey(Address, related_name="%(class)s_send_a", on_delete=models.PROTECT,)
	sender = models.ForeignKey(Profile, related_name="%(class)s_sender", on_delete=models.PROTECT)

	# receiver_mode = models.SmallIntegerField(choices=transport_modes, verbose_name="Drop-off mode: ")
	# receiver_number = models.CharField(max_length=32, validators=[phone_regex], verbose_name="Phone number for pickup: ")
	receiver_address = models.ForeignKey(Address, related_name="%(class)s_receive_a", on_delete=models.PROTECT)

	status_code = [(0, "Still accepting offers"), (1, "A deal is in progress"), (2, "A deal is completed"),
				   (3, "The package has been dropped off"), (4, "The package is with the courier"),
				   (5, "The courier has delivered the package"), (6, "The package has been received"), (7, "Cancelled"), (8, "Rated"), (9, "Attached")]
	status = models.SmallIntegerField(choices=status_code, default=0)
	courier = models.ForeignKey(CourierAd, related_name="%(class)s_courier", on_delete=models.PROTECT, null=True, default=None)


@admin.display(description="Sender Full Name")
def get_package_full_name(obj):
	return "%s %s" % (obj.sender.name_f.upper(), obj.sender.name_l.upper())


class PackageAdmin(admin.ModelAdmin):
	list_display = (get_package_full_name, get_status)


class Message(models.Model):
	sender = models.ForeignKey(Profile, related_name="%(class)s_sender", on_delete=models.PROTECT)
	img = models.ImageField(verbose_name="Attach an image: ", blank=True)
	text = models.CharField(verbose_name="Message body: ", max_length=240)
	regarding_code = models.SmallIntegerField(choices=[(1, "Courier Ad"), (2, "Package Ad")])
	regarding_uuid = models.UUIDField()
	time = models.DateTimeField(auto_now=True)
	visible = models.BooleanField(default=True)


class MessageAdmin(admin.ModelAdmin):
	list_display = (get_package_full_name, "time")

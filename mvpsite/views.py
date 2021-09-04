from django import forms
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.shortcuts import render, redirect
from .models import PackageAd, CourierAd, countries, Profile, KYCAuth, Address
from django.contrib.auth.models import User


# Create your views here.
def home(request):
	if not request.user.is_authenticated or not test_kyc_exists(request):
		return redirect("/mvp/user/new/")
	else:
		return redirect("/mvp/user/dash/")


def test_kyc_exists(request):
	if not Profile.objects.filter(user=request.user).exists():
		return False
	else:
		user = Profile.objects.get(user=request.user)
	if not KYCAuth.objects.filter(user=user).exists():
		return False
	return True


def test_kyc(request):
	return True
	try:
		user = Profile.objects.get(user=request.user)
		return KYCAuth.objects.get(user=user).status == 1
	except Profile.DoesNotExist:
		return False


def get_full_name(request):
	if not request.user.is_authenticated:
		return "<p>Welcome! Please <strong><a href='/mvp/user/new/'>make an account</a></strong></p>"
	elif not test_kyc_exists(request):
		return "<p>It appears we are missing your KYC information. Please <strong><a href='/user/new/'>submit it here</strong></a></p>"
	elif not test_kyc(request):
		return "<p>Welcome!  Your account is not yet authenticated.  Your current status is <strong>%s</strong>.</p>" %KYCAuth.objects.get(user=Profile.objects.get(user=request.user)).get_status_display()
	else:
		p = Profile.objects.get(user=request.user)
		return "<p>Welcome <strong>%s %s</strong></p>" % (p.name_f, p.name_l)


# Courier
class CourierFilter(forms.Form):
	weight = forms.FloatField(label="Minimum Weight (lb): ")
	price_max = forms.FloatField(label="Maximum Price (USD): ")
	depart_country = forms.ChoiceField(choices=countries, label="From: ")
	receive_country = forms.ChoiceField(choices=countries, label="To: ")


def courier_ads(request):
	ads = CourierAd.objects.filter(status__lte=1)
	if request.method == "POST":
		form = CourierFilter(request.POST)
		if form.is_valid():
			ads = ads.filter(package_weight__gte=form.cleaned_data["weight"],
							 package_price_min__lte=form.cleaned_data["price_max"],
							 dep_country__exact=form.cleaned_data["receive_country"],
							 dest_country__exact=form.cleaned_data["depart_country"])
	else:
		form = CourierFilter()
	return render(request, "mvp/templates/courier.html", {"filter": form, "ads": ads, "u": get_full_name(request)})


class CourierAdCreate(forms.ModelForm):
	class Meta:
		model = CourierAd
		exclude = ["id", "courier", "status"]


def courier_create(request):
	if not test_kyc(request):
		return redirect("/mvp/")
	if request.method == "POST":
		form = CourierAdCreate(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.user = Profile.objects.get(user=request.user)
			form.save()
	else:
		form = CourierAdCreate()
	return render(request, "mvp/templates/embed-form.html", {"name": "New Courier Ad", "forms": [("", form)]})


# Packages
class PackageFilter(forms.Form):
	weight = forms.FloatField(label="Maximum Weight (lb): ")
	price_min = forms.FloatField(label="Minimum Price (USD): ")
	depart_country = forms.ChoiceField(choices=countries, label="From: ")
	receive_country = forms.ChoiceField(choices=countries, label="To: ")


def package_ads(request):
	ads = PackageAd.objects.filter(status__lte=1)
	if request.method == "POST":
		form = PackageFilter(request.POST)
		if form.is_valid():
			ads = ads.filter(package_weight__lte=form.cleaned_data["weight"],
							 package_price_max__gte=form.cleaned_data["price_min"],
							 receiver_address__country__exact=form.cleaned_data["receive_country"],
							 sender_address__country__exact=form.cleaned_data["depart_country"])
	else:
		form = PackageFilter()
	return render(request, "mvp/templates/package.html", {"filter": form, "ads": ads, "u": get_full_name(request)})


class PackageAdCreate(forms.ModelForm):
	class Meta:
		model = PackageAd
		exclude = ["id", "sender", "sender_address", "receiver_address", "status", "courier"]


def package_create(request):
	if not test_kyc(request):
		return redirect("/mvp/")
	if request.method == "POST":
		form = CourierAdCreate(request.POST)
		addy1 = AddressForm(request.POST)
		addy2 = AddressForm2(request.POST)
		if form.is_valid() and addy1.is_valid() and addy2.is_valid():
			form = form.save(commit=False)
			form.sender_address = addy1.save()
			form.receiver_address = addy2.save()
			form.sender = Profile.objects.get(user=request.user)
			form.save()
	else:
		form = CourierAdCreate()
		addy1 = AddressForm()
		addy2 = AddressForm2()
	return render(request, "mvp/templates/embed-form.html", {"name": "New Package Ad", "forms": [("", form), ("Receiver address", addy2), ("Pickup address", addy1)]})


# User Management
def log_in(request):
	if request.method == "POST":
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("/mvp/")
	else:
		form = AuthenticationForm()
	return render(request, "mvp/templates/basic-form.html", {"title": "Please Log In", "btn": "Log In", "form": form})


class UserCreationForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(), label="Password", required=True)
	password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm password", required=True)

	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']

	def clean(self):
		# super(UserCreationForm, self).clean()
		if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
			raise forms.ValidationError("Passwords do not match!")

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.username = self.cleaned_data["email"]
		if commit:
			user.save()
		return user


class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['profile', 'role', 'phone_number', "referer"]


class AddressForm(ModelForm):
	class Meta:
		model = Address
		fields = ['address', 'address_2', 'state', 'city', 'country', 'postal_code']


class AddressForm2(ModelForm):
	address1 = forms.CharField(max_length=32, label="Address: ")
	address1_2 = forms.CharField(max_length=32, label="Address Line 2: ", required=False)
	state1 = forms.CharField(max_length=32, label="State/Province: ")
	city1 = forms.CharField(max_length=32, label="City: ")
	country1 = forms.ChoiceField(choices=countries, label="Country: ")
	postal_code1 = forms.CharField(max_length=32, label="Postal Code: ")

	class Meta:
		model = Address
		fields = ['address1', 'address1_2', 'state1', 'city1', 'country1', 'postal_code1']

	def save(self, commit=True):
		addy = super(AddressForm2, self).save(commit=False)
		addy.address = self.cleaned_data["address1"]
		addy.address_2 = self.cleaned_data["address1_2"]
		addy.state = self.cleaned_data["state1"]
		addy.city = self.cleaned_data["city1"]
		addy.country = self.cleaned_data["country1"]
		addy.postal_code = self.cleaned_data["postal_code1"]
		if commit:
			addy.save()
		return addy


class KYCForm(ModelForm):
	class Meta:
		model = KYCAuth
		fields = ['f_lic', 'b_lic', 'mail_item']


def create_user(request):
	if not request.user.is_authenticated:
		if request.method == "POST":
			form = UserCreationForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data.get("email")
				password = form.cleaned_data.get("password")
				form = form.save(commit=False)
				form.set_password(password)
				form.save()
				user = authenticate(request, username=username, password=password)
				login(request, user)
				return redirect("/mvp/user/new/")
		else:
			form = UserCreationForm()
		return render(request, "mvp/templates/sign-up.html", {"form": form})
	elif not Profile.objects.filter(user=request.user).exists():
		if request.method == "POST":
			form1 = ProfileForm(request.POST, request.FILES)
			form2 = AddressForm(request.POST)
			if form1.is_valid() and form2.is_valid():
				form1 = form1.save(commit=False)
				form1.user = request.user
				form1.name_f = request.user.first_name
				form1.name_l = request.user.last_name
				form2 = form2.save()
				form1.address = form2
				form1.save()
				return redirect("/mvp/user/new/")
		else:
			form1 = ProfileForm()
			form2 = AddressForm()
		return render(request, "mvp/templates/prof-address-form.html", {"title": "Please complete your account", "btn": "Next", "form1": form1, "form2": form2})
	elif not KYCAuth.objects.filter(user=Profile.objects.get(user=request.user)).exists():
		if request.method == "POST":
			form = KYCForm(request.POST, request.FILES)
			if form.is_valid():
				form = form.save(commit=False)
				form.user = Profile.objects.get(user=request.user)
				form.save()
				return redirect("/mvp/")
		else:
			form = KYCForm()
		return render(request, "mvp/templates/basic-form.html", {"kyc": True, "title": "KYC is required.  Please submit the required information "
															"to activate your account", "btn": "Finish Setup", "form": form})
	return redirect("/mvp/")


def edit_profile(request):
	if not test_kyc(request):
		return redirect("/mvp/")
	user = Profile.objects.get(user=request.user)
	if request.method == "POST":
		form1 = ProfileForm(request.POST, request.FILES, instance=user)
		form2 = AddressForm(request.POST, instance=user.address)
		if form1.is_valid() and form2.is_valid():
			form1 = form1.save(commit=False)
			form1.address = form2.save()
			form1.save()
			return redirect("/mvp/")
	else:
		form1 = ProfileForm(instance=user)
		form2 = AddressForm(instance=user.address)
	return render(request, "mvp/templates/embed-form.html", {"name": "Edit Profile", "forms": [("", form1), ("Edit address", form2)]})
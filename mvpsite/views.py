from django import forms
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.shortcuts import render, redirect
from .models import Message, PackageAd, CourierAd, countries, Profile, KYCAuth, Address, get_courier_full_name, get_package_full_name
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


def get_deals(profile):
	if profile.role == 0:
		packs = PackageAd.objects.filter(sender=profile)
		ads = []
		in_progress = []
		complete = []
		for pack in packs:
			if pack.status < 2:
				ads.append(pack)
			elif pack.status < 6 or (pack.status == 9 and pack.courier.status != 8):
				in_progress.append(pack)
			else:
				complete.append(pack)
	else:
		courierAds = CourierAd.objects.filter(courier=profile)
		ads = []
		in_progress = []
		complete = []
		for courier in courierAds:
			if courier.status < 2:
				ads.append(courier)
			elif courier.status < 4 or (courier.status == 9 and courier.package.status != 8):
				in_progress.append(courier)
			else:
				complete.append(courier)
	return profile.role == 0, {"ads": ads, "deals_current": in_progress, "deals_completed": complete}


def dashboard(request):
	user = Profile.objects.get(user=request.user)
	role, con = get_deals(user)
	con["u"] = get_full_name(request)
	if role:
		return render(request, "mvp/templates/dashboard_sender.html", con)
	else:
		return render(request, "mvp/templates/dashboard_courier.html", con)


# Both ad functions
def get_owner_controls(request, ad, courier):
	if courier:
		if test_kyc(request):
			if ad.courier == Profile.objects.get(user=request.user):
				controls = []
				if ad.status < 4:
					controls.append({"name": "Cancel", "url": "/mvp/couriers/cancel/%s" % ad.id})
				if ad.status == 1:
					controls.append({"name": "Revert", "url": "/mvp/couriers/revert/%s" % ad.id})
					controls.append({"name": "Accept Deal", "url": "/mvp/couriers/accept/%s" % ad.id})
				elif 4 > ad.status > 1:
					nex = ad.status_code[ad.status + 1][1]
					controls.append({"name": "Mark status as %s" % nex, "url": "/mvp/couriers/next/%s" % ad.id})
				return controls
	else:
		if test_kyc(request):
			if ad.sender == Profile.objects.get(user=request.user):
				controls = []
				if ad.status < 6:
					controls.append({"name": "Cancel", "url": "/mvp/packages/cancel/%s" % ad.id})
				if ad.status == 1:
					controls.append({"name": "Revert", "url": "/mvp/packages/revert/%s" % ad.id})
					controls.append({"name": "Accept Deal", "url": "/mvp/packages/accept/%s" % ad.id})
				elif 6 > ad.status > 1:
					nex = ad.status_code[ad.status + 1][1]
					controls.append({"name": "Mark status as %s" % nex, "url": "/mvp/packages/next/%s" % ad.id})
				return controls
	return None


def get_messages(request, ad, courier):
	if not test_kyc(request):
		return None
	mess = Message.objects.filter(regarding_uuid=ad.id, visible=True)
	if courier:
		if ad.status > 0:
			mess = mess.filter(regarding_code=1)
			if ad.package is None:
				return None
			elif ad.package.sender != Profile.objects.get(user=request.user) and ad.courier != Profile.objects.get(user=request.user):
				return None
		elif ad.status == 0 and ad.courier == Profile.objects.get(user=request.user):
			return None

	else:
		mess = mess.filter(regarding_code=0)
		if ad.status > 0:
			if ad.courier is None:
				return None
			elif ad.sender != Profile.objects.get(user=request.user) and ad.courier.courier != Profile.objects.get(user=request.user):
				return None
		elif ad.status == 0 and ad.sender == Profile.objects.get(user=request.user):
			return None

	messages = []
	for m in mess:
		messages.append({"name": "%s %s" % (m.sender.name_f.upper(), m.sender.name_l.upper()), "time": m.time, "text": m.text})
		if m.img is not None:
			messages[-1]["image"] = m.img
	return messages


class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ["img", "text"]


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
		exclude = ["id", "courier", "status", "package"]


def courier_ad(request, id):
	ad = CourierAd.objects.get(id=id)
	btn = "Send message to start a deal" if ad.status == 0 else "Send"
	context = {"no_options": False, "user": ad.courier.id, "name": "%s %s" % (ad.courier.name_f, ad.courier.name_l), "ad": ad, "messages": get_messages(request, ad, True),
			   "owner_links": get_owner_controls(request, ad, True), "u": get_full_name(request), "btn": btn}
	if request.method == "POST":
		form = MessageForm(request.POST, request.FILES)
		if form.is_valid():
			form = form.save(commit=False)
			form.sender = Profile.objects.get(user=request.user)
			form.regarding_uuid = ad.id
			form.regarding_code = 1
			form.save()
			if ad.status == 0:
				package = PackageAd.objects.get(id=request.POST["package"])
				ad.package = package
				package.courier = ad
				package.status = 9
				ad.status = 1
				ad.save()
				package.save()
			return redirect(request.path_info)
	else:
		form = MessageForm()
		if ad.status == 0:
			packages = PackageAd.objects.filter(sender=Profile.objects.get(user=request.user), status=0)
			form.fields['package'] = forms.ChoiceField(choices=[(p.id, p.receiver_address.address) for p in packages], label="Choose package: ")
			context["no_options"] = len(form.fields['package'].choises) == 0

	context["form"] = form
	context["message_on"] = context["messages"] is not None
	return render(request, "mvp/templates/ad-courier.html", context)


def courier_create(request):
	if not test_kyc(request):
		return redirect("/mvp/")
	if request.method == "POST":
		form = CourierAdCreate(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.courier = Profile.objects.get(user=request.user)
			form.save()
			redirect("/mvp/")
	else:
		form = CourierAdCreate()
	return render(request, "mvp/templates/embed-form.html", {"name": "New Courier Ad", "forms": [("", form)], "u": get_full_name(request)})


def courier_next(request, id):
	courier = CourierAd.objects.get(id=id)
	if courier.courier == Profile.objects.get(user=request.user) and courier.status < 7:
		courier.status += 1
		courier.save()
	return redirect("/mvp/couriers/%s" % courier.id)


def courier_cancel(request, id):
	courier = CourierAd.objects.get(id=id)
	if courier.courier == Profile.objects.get(user=request.user) and courier.status < 6:
		courier.status = 7
		courier.save()
	return redirect("/mvp/couriers/%s" % courier.id)


def courier_accept(request, id):
	courier = CourierAd.objects.get(id=id)
	if courier.courier == Profile.objects.get(user=request.user) and courier.status == 1:
		courier.status = 2
		courier.save()
	return redirect("/mvp/couriers/%s" % courier.id)


def courier_revert(request, id):
	courier = CourierAd.objects.get(id=id)
	if courier.courier == Profile.objects.get(user=request.user) and courier.status == 1:
		courier.package = None
		courier.status = 0
		courier.save()
	mess = Message.objects.filter(regarding_uuid=courier.id, visible=True, regarding_code=1)
	for m in mess:
		m.visible = False
		m.save()
	return redirect("/mvp/couriers/%s" % courier.id)


# Packages
class PackageFilter(forms.Form):
	weight = forms.FloatField(label="Maximum Weight (lb): ")
	price_min = forms.FloatField(label="Minimum Price (USD): ")
	depart_country = forms.ChoiceField(choices=countries, label="From: ")
	receive_country = forms.ChoiceField(choices=countries, label="To: ")


def package_ad(request, id):
	ad = PackageAd.objects.get(id=id)
	btn = "Send message to start a deal" if ad.status == 0 else "Send"
	context = {"no_options": False, "user": ad.sender.id, "name": "%s %s" % (ad.sender.name_f, ad.sender.name_l), "ad": ad, "messages": get_messages(request, ad, False),
			   "owner_links": get_owner_controls(request, ad, False), "u": get_full_name(request), "btn": btn}
	if request.method == "POST":
		form = MessageForm(request.POST, request.FILES)
		if form.is_valid():
			form = form.save(commit=False)
			form.sender = Profile.objects.get(user=request.user)
			form.regarding_uuid = ad.id
			form.regarding_code = 0
			form.save()
			if ad.status == 0:
				courier = CourierAd.objects.get(id=request.POST["courier"])
				ad.courier = courier
				courier.package = ad
				courier.status = 9
				ad.status = 1
				ad.save()
				courier.save()
			return redirect(request.path_info)
	else:
		form = MessageForm()
		if ad.status == 0:
			couriers = CourierAd.objects.filter(courier=Profile.objects.get(user=request.user), status=0)
			form.fields['courier'] = forms.ChoiceField(choices=[(c.id, "%s to %s" % (c.dep_airport, c.dest_airport)) for c in couriers], label="Choose package: ")
			context["no_options"] = len(form.fields['courier'].choises) == 0

	context["form"] = form
	context["message_on"] = context["messages"] is not None
	return render(request, "mvp/templates/ad-package.html", context)


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
		form = PackageAdCreate(request.POST, request.FILES)
		addy1 = AddressForm(request.POST)
		addy2 = AddressForm2(request.POST)
		if form.is_valid() and addy1.is_valid() and addy2.is_valid():
			form = form.save(commit=False)
			form.sender_address = addy1.save()
			form.receiver_address = addy2.save()
			form.sender = Profile.objects.get(user=request.user)
			form.save()
			return redirect("/mvp/")
	else:
		form = PackageAdCreate()
		addy1 = AddressForm()
		addy2 = AddressForm2()
	return render(request, "mvp/templates/embed-form.html", {"name": "New Package Ad", "forms": [("", form), ("Drop off address", addy2), ("Pickup address", addy1)], "u": get_full_name(request)})


def package_next(request, id):
	pack = PackageAd.objects.get(id=id)
	if pack.sender == Profile.objects.get(user=request.user) and pack.status < 7:
		pack.status += 1
		pack.save()
	return redirect("/mvp/packages/%s" % pack.id)


def package_cancel(request, id):
	pack = PackageAd.objects.get(id=id)
	if pack.sender == Profile.objects.get(user=request.user) and pack.status < 4:
		pack.status = 7
		pack.save()
	return redirect("/mvp/packages/%s" % pack.id)


def package_accept(request, id):
	pack = PackageAd.objects.get(id=id)
	if pack.sender == Profile.objects.get(user=request.user) and pack.status == 1:
		pack.status = 2
		pack.save()
	return redirect("/mvp/packages/%s" % pack.id)


def package_revert(request, id):
	pack = PackageAd.objects.get(id=id)
	if pack.sender == Profile.objects.get(user=request.user) and pack.status == 1:
		pack.courier = None
		pack.status = 0
		pack.save()
	mess = Message.objects.filter(regarding_uuid=pack.id, visible=True, regarding_code=1)
	for m in mess:
		m.visible = False
		m.save()
	return redirect("/mvp/packages/%s" % pack.id)


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


def profile(request, id):
	prof = Profile.objects.get(id=id)
	return render(request, "mvp/templates/profile.html", {"pname": "%s %s" % (prof.name_f.upper(), prof.name_l.upper()), "role": prof.get_role_display(), "profile": prof, "edit": prof==Profile.objects.get(user=request.user), "u": get_full_name(request)})


def current_profile(request):
	return redirect("/mvp/user/%s" % Profile.objects.get(user=request.user).id)


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
	return render(request, "mvp/templates/embed-form.html", {"name": "Edit Profile", "forms": [("", form1), ("Edit address", form2)], "u": get_full_name(request)})


def user_ads(request):
	if Profile.objects.get(user=request.user).role == 0:
		return redirect("/mvp/couriers")
	else:
		return redirect("/mvp/packages")


class RatingForm(forms.Form):
	rating = forms.IntegerField(label="Rating (x/10): ", max_value=10, min_value=0)


def rate_user(request, uid, cat, adid):
	prof = Profile.objects.get(id=uid)
	if request.method == "POST":
		form = RatingForm(request.POST)
		if form.is_valid():
			prof.rating = (form.cleaned_data["rating"] + (prof.rating * prof.num_of_ratings))/(prof.num_of_ratings + 1)
			prof.num_of_ratings += 1
			if cat == 1:
				ad = CourierAd.objects.get(id=adid)
			else:
				ad = PackageAd.objects.get(id=adid)
			if ad.status == 8:
				return redirect("/mvp/")
			ad.status = 8
			ad.save()
			prof.save()
			return redirect("/mvp/")
	else:
		form = RatingForm()
	return render(request, "mvp/templates/embed-form.html", {"name": "Rate %s" % prof.name_f, "forms": [("", form)], "u": get_full_name(request)})
from django import forms
from django.shortcuts import render
from .models import PackageAd, CourierAd, countries


# Create your views here.
def test(request):
	return render(request, "mvp/form.html")


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
	return render(request, "mvp/courierAds.html", {"filter": form, "ads": ads})


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
	return render(request, "mvp/packageAds.html", {"filter": form, "ads": ads})
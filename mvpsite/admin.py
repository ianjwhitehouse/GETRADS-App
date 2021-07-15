from django.contrib import admin
from .models import KYCAuth, KYCAdmin, Profile, ProfileAdmin, CourierAd, CourierAdmin, PackageAd, PackageAdmin, Address, \
	Message, MessageAdmin

# Register your models here.
admin.site.register(KYCAuth, KYCAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CourierAd, CourierAdmin)
admin.site.register(PackageAd, PackageAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Address)
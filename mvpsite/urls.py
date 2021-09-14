"""GetradsDjangoWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
	path('', home),
	path('packages/<uuid:id>', package_ad),
	path('packages/', package_ads),
	path('packages/new/', package_create),
	path('packages/next/<uuid:id>', package_next),
	path('packages/cancel/<uuid:id>', package_cancel),
	# path('packages/search/<uuid:id>', package_cancel),
	path('couriers/', courier_ads),
	path('couriers/uuid:id', courier_ad),
	path('couriers/new/', courier_create),
	path('couriers/next/<uuid:id>', courier_next),
	path('couriers/cancel/<uuid:id>', courier_cancel),
	path('couriers/accept/<uuid:id>', courier_accept),
	path('couriers/revert/<uuid:id>', courier_revert),
	path('user/', current_profile),
	path('user/<uuid:id>', profile),
	path('user/login/', log_in),
	path('user/new/', create_user),
	path('user/edit/', edit_profile),
	path('user/dash/', dashboard),
	path('user/ads/', user_ads),
	path('user/rate/<uuid:uid>/<int:cat>/<uuid:adid>', rate_user),
]

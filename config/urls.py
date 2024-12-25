"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from config.admin import custom_admin_site
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings


admin.site.site_header = 'Admin'
admin.site.site_title = 'Flight'
admin.site.index_title = 'Manage Admin'

# admin.site.site_header()
urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('',include('frontend.urls')),
    path('payment/', include("payment.urls"),name="payment"),
    path('accounts/', include('accounts.urls'),name="accounts"),
    path('flight/', include('flights.urls') , name="flight"),
    path('booking/', include('booking.urls') , name="booking"),

]
    


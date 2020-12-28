from django.contrib import admin

# Register your models here.
from django.apps import apps
from rest_framework.authtoken.models import TokenProxy

from api.models import User, Tickets, UserTickets

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

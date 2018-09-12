from django.contrib import admin

from .models import Station, User, Trip


admin.site.register(Station)
admin.site.register(User)
admin.site.register(Trip)

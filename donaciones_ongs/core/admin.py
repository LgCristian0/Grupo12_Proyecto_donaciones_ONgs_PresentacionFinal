from django.contrib import admin
from .models import ONG, Donante, Campaña, Donacion

# Register your models here.

admin.site.register(ONG)
admin.site.register(Donante)
admin.site.register(Campaña)
admin.site.register(Donacion)

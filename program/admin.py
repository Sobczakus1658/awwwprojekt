from django.contrib import admin

from .models import Katalog, Plik, Sekcja_pliku, Rodzaj_sekcji


admin.site.register(Katalog)
admin.site.register(Plik)
admin.site.register(Sekcja_pliku)
admin.site.register(Rodzaj_sekcji)
# Register your models here.

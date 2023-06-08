from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
class Katalog(models.Model):
    rodzic = models.IntegerField(default = 0)
    nazwa = models.CharField(max_length=20)
    opcjonalny_opis = models.TextField(blank=True, default='')
    data_utworzenia = models.DateTimeField(auto_now = True)
    wlasciciel = models.ForeignKey(User, on_delete = models.CASCADE, default=None, blank =True, null = True)
    znacznik_dostepnosci = models.BooleanField(default=True)
    data_zmiany_znacznika = models.DateTimeField(auto_now = True)
    data_ostatniej_zmiany_zawartosci = models.DateTimeField(auto_now = True)

    @classmethod
    def create(cls, katalog_nazwa, rodzic, user):
        katalog = Katalog(
            rodzic = rodzic,
            wlasciciel = user,
            nazwa = katalog_nazwa,
        )
        return katalog
    
    def __str__(self):
        wynik = f'<li>{self.nazwa.replace("<", "&lt;").replace(">", "&gt;")}</li>'
        podkatalogi = Katalog.objects.filter(rodzic=self.id, znacznik_dostepnosci=True)
        podpliki = Plik.objects.filter(rodzic=self.id, znacznik_dostepnosci=True)
        if podkatalogi or podpliki :
            wynik += '<ul>'
            if podkatalogi:
                for element in podkatalogi:
                    if element != self:
                        wynik += element.__str__()
            if podpliki:
                for element in podpliki:
                    wynik += element.__str__()
            wynik += '</ul>'
        return wynik


class Plik(models.Model):
    wlasciciel = models.ForeignKey(User, on_delete = models.CASCADE, default=None, blank =True, null = True)
    nazwa = models.CharField(max_length=10)
    tresc = models.TextField(default ='')
    rodzic = models.IntegerField(default = 0)
    opcjonalny_opis = models.TextField()
    data_utworzenia = models.DateField(auto_now = True)
    znacznik_dostepnosci = models.BooleanField(default=True)
    data_zmiany_znacznika = models.DateField(auto_now = True)
    data_ostatniej_zmiany_zawartosci = models.DateField(auto_now = True)

    @classmethod
    def create(cls, plik_nazwa, rodzic, tresc, user):
        plik = Plik(
            nazwa = plik_nazwa,
            tresc = tresc,
            rodzic = rodzic,
            wlasciciel = user,
            # znacznik_dostepnosci = True,
        )
        return plik
    
    def __str__(self):
        return '<li>' + '<a href="http://127.0.0.1:8000/'+str(self.id)+'">' + self.nazwa+ '</a>' + '</li>'

class Rodzaj_sekcji(models.Model):
    nazwa = models.CharField(max_length= 50)
    @classmethod
    def create(cls, nazwa):
        rodzaj_sekcji = Rodzaj_sekcji(nazwa = nazwa)
        return rodzaj_sekcji

    def __str__(self):
        return self.nazwa

class Status_sekcji(models.Model):
    nazwa = models.CharField(max_length= 50)
    @classmethod
    def create(cls, nazwa):
        status_sekcji = Status_sekcji(nazwa = nazwa)
        return status_sekcji

    def __str__(self):
        return self.nazwa

class Dane_statusu(models.Model):
    nazwa = models.CharField(max_length= 50)
    @classmethod
    def create(cls, nazwa):
        dane_statusu = Dane_statusu(nazwa = nazwa)
        return dane_statusu

    def __str__(self):
        return self.nazwa


class Sekcja_pliku(models.Model):
    id_ojca_pliku = models.IntegerField(default=0)
    opcjonalna_nazwa = models.CharField(max_length=50, default='')
    opcjonalny_opis = models.TextField (default='')
    data_utworzenia = models.DateField(auto_now = True)
    znacznik_dostepnosci = models.BooleanField(default=True)
    poczatek_sekcji = models.IntegerField(default=0)
    koniec_sekcji = models.IntegerField(default=0)
    rodzaj_sekcji = models.IntegerField(default = 0)
    status_sekcji = models.IntegerField(default = 0)
    dane_statusu = models.IntegerField(default = 0)
    tresc = models.TextField()
    def __str__(self):
        return self.opcjonalna_nazwa
    @classmethod
    def create(cls, nazwa_sekcji, opis_sekcji, tresc_sekcji, poczatek_sekcji, koniec_sekcji, id_rodzaju_sekcji, rodzic):
        sekcja_pliku = Sekcja_pliku(
            opcjonalna_nazwa = nazwa_sekcji,
            id_ojca_pliku = rodzic,
            opcjonalny_opis = opis_sekcji,
            rodzaj_sekcji = id_rodzaju_sekcji ,
            znacznik_dostepnosci = 1,
            poczatek_sekcji = poczatek_sekcji,
            koniec_sekcji = koniec_sekcji,
            tresc = tresc_sekcji,
        )
        return sekcja_pliku


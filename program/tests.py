from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json
from .views import pobierz_do_tworzenia_pliku
from .models import Sekcja_pliku, Rodzaj_sekcji , Status_sekcji, Dane_statusu
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from .models import Plik, Katalog
from django.http import HttpRequest
from django.test import RequestFactory
from program.views import wypisz_fragment, podziel, usun_plik
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
import unittest
import json
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from program.models import Katalog
from django.test import RequestFactory
from django.urls import reverse
from program.models import Sekcja_pliku, Plik
from program.views import pobierz_sekcje, podziel
from .views import pobierz_do_usuwania_katalogu, pobierz_niezalezne_pliki
from .forms import LoginForm
from .views import zmien_zmienna, login_view,  stworz_plik
from .views import pobierz_do_tworzenia_pliku, setValue
from .views import pobierz_do_tworzenia_katalogi
from .views import logowanie, wylogowanie,pobierz_katalogi
from .views import rodzaj_linii, usun_sekcje, usun_plik
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http import FileResponse
from unittest.mock import patch
import re
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Plik
from .views import kompiluj
from django.test.client import RequestFactory


from program.views import pobierz


class SekcjaPlikuTest(TestCase):
    def setUp(self):
        self.nazwa_sekcji = 'Testowa sekcja'
        self.opis_sekcji = 'Opis testowej sekcji'
        self.tresc_sekcji = 'Tresc testowej sekcji'
        self.poczatek_sekcji = 0
        self.koniec_sekcji = 10
        self.id_rodzaju_sekcji = 1
        self.rodzic = 1

    def test_create_sekcja_pliku(self):
        sekcja_pliku = Sekcja_pliku.create(
            self.nazwa_sekcji,
            self.opis_sekcji,
            self.tresc_sekcji,
            self.poczatek_sekcji,
            self.koniec_sekcji,
            self.id_rodzaju_sekcji,
            self.rodzic
        )

        self.assertEqual(sekcja_pliku.opcjonalna_nazwa, self.nazwa_sekcji)
        self.assertEqual(sekcja_pliku.id_ojca_pliku, self.rodzic)
        self.assertEqual(sekcja_pliku.opcjonalny_opis, self.opis_sekcji)
        self.assertEqual(sekcja_pliku.rodzaj_sekcji, self.id_rodzaju_sekcji)
        self.assertEqual(sekcja_pliku.poczatek_sekcji, self.poczatek_sekcji)
        self.assertEqual(sekcja_pliku.koniec_sekcji, self.koniec_sekcji)
        self.assertEqual(sekcja_pliku.tresc, self.tresc_sekcji)

        # Dodaj inne asercje, które chcesz przetestować dla modelu

        # Przykład:
        self.assertEqual(sekcja_pliku.znacznik_dostepnosci, 1)
        self.assertEqual(sekcja_pliku.status_sekcji, 0)
        self.assertEqual(sekcja_pliku.dane_statusu, 0)

class RodzajSekcjiTestCase(TestCase):
    def setUp(self):
        self.nazwa = "Testowy rodzaj sekcji"

    def test_create_rodzaj_sekcji(self):
        rodzaj_sekcji = Rodzaj_sekcji.create(self.nazwa)
        self.assertEqual(rodzaj_sekcji.nazwa, self.nazwa)

class StatusSekcjiTestCase(TestCase):
    def setUp(self):
        self.nazwa = "Testowy status sekcji"

    def test_create_status_sekcji(self):
        status_sekcji = Status_sekcji.create(self.nazwa)
        self.assertEqual(status_sekcji.nazwa, self.nazwa)

class DaneStatusuTestCase(TestCase):
    def setUp(self):
        self.nazwa = "Testowe dane statusu"

    def test_create_dane_statusu(self):
        dane_statusu = Dane_statusu.create(self.nazwa)
        self.assertEqual(dane_statusu.nazwa, self.nazwa)

class PlikTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.plik_nazwa = 'Testowy plik'
        self.rodzic = 1
        self.tresc = 'Testowa treść'
    
    def test_create_plik(self):
        plik = Plik.create(self.plik_nazwa, self.rodzic, self.tresc, self.user)
        plik.save()
        self.assertEqual(plik.nazwa, self.plik_nazwa)
        self.assertEqual(plik.rodzic, self.rodzic)
        self.assertEqual(plik.tresc, self.tresc)
        self.assertEqual(plik.wlasciciel, self.user)
        self.assertEqual(plik.znacznik_dostepnosci, True)
        self.assertIsInstance(plik.data_utworzenia, date)
        self.assertIsInstance(plik.data_zmiany_znacznika, date)
        self.assertIsInstance(plik.data_ostatniej_zmiany_zawartosci, date)

    def test_str_representation(self):
        plik = Plik(
            nazwa=self.plik_nazwa,
            rodzic=self.rodzic,
            tresc=self.tresc,
            wlasciciel=self.user,
            znacznik_dostepnosci=True
        )
        plik.save()
        expected_str = f'<li><a href="http://127.0.0.1:8000/{plik.id}">{plik.nazwa}</a></li>'
        self.assertEqual(str(plik), expected_str)

class KatalogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.katalog_nazwa = 'Testowy katalog'
        self.rodzic = 1

    def test_create_katalog(self):
        katalog = Katalog.create(self.katalog_nazwa, self.rodzic, self.user)
        katalog.save()
        self.assertEqual(katalog.nazwa, self.katalog_nazwa)
        self.assertEqual(katalog.rodzic, self.rodzic)
        self.assertEqual(katalog.wlasciciel, self.user)
        self.assertEqual(katalog.znacznik_dostepnosci, True)
        self.assertIsInstance(katalog.data_utworzenia, date)
        self.assertIsInstance(katalog.data_zmiany_znacznika, date)
        self.assertIsInstance(katalog.data_ostatniej_zmiany_zawartosci, date)
     


class PobierzDoUsuwaniaKataloguTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.katalog1 = Katalog.objects.create(nazwa='Katalog 1', znacznik_dostepnosci=1, wlasciciel=self.user)
        self.katalog2 = Katalog.objects.create(nazwa='Katalog 2', znacznik_dostepnosci=1, wlasciciel=self.user)

    def test_pobierz_do_usuwania_katalogu(self):
        request = self.factory.get(reverse('program:pobierz_do_usuwania_katalogu'))
        request.user = self.user

        response = pobierz_do_usuwania_katalogu(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

        json_data = json.loads(response.content)
        self.assertIn('html', json_data)

        html = json_data['html']
        self.assertIsInstance(html, str)
        self.assertEqual(html, '<input type="radio" name="rodzic" id="1" value="1"><label for="1">Katalog 1</label><br><input type="radio" name="rodzic" id="2" value="2"><label for="2">Katalog 2</label><br><input type="submit" value="Usun">')
        self.assertEqual(response['content-type'], 'application/json')
        self.assertIn('<input type="submit" value="Usun">', html)

class LoginFormTest(TestCase):
    def test_login_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = LoginForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'testuser')
        self.assertEqual(form.cleaned_data['password'], 'testpassword')

class ZmienZmiennaTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_zmien_zmienna(self):
        url = reverse('program:zmien_zmienna')
        request = self.factory.post(url, data='{"nazwa": "standard", "standard": "value"}', content_type='application/json')

        response = zmien_zmienna(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

        json_data = json.loads(response.content)
        self.assertIn('nazwa', json_data)
        self.assertEqual(json_data['nazwa'], 'standard')

class PobierzDoTworzeniaPlikuTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_pobierz_do_tworzenia_pliku(self):
        url = reverse('program:pobierz_do_tworzenia_pliku')
        request = self.factory.get(url)
        request.user = self.user

        response = pobierz_do_tworzenia_pliku(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

        json_data = json.loads(response.content)
        self.assertIn('html', json_data)

        html = json_data['html']
        self.assertIn('<input type="radio" name="rodzic" id="', html)
        self.assertIn('<label for="', html)
        self.assertIn('<input type="file" name="nazwa" accept=".c">', html)
        self.assertIn('<input type="submit" value="Dodaj">', html)
class PobierzDoTworzeniaKatalogiTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_pobierz_do_tworzenia_katalogi(self):
        url = reverse('program:pobierz_do_tworzenia_katalogi')
        request = self.factory.get(url)
        request.user = self.user

        response = pobierz_do_tworzenia_katalogi(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

        json_data = json.loads(response.content)
        self.assertIn('html', json_data)

        html = json_data['html']
        self.assertIn('<input type="radio" name="rodzic" id="', html)
        self.assertIn('<label for="', html)
        self.assertIn('<input type="radio" name="rodzic" id="0" value="0">', html)
        self.assertIn('<label for="0" name="rodzic">Niezależny katalog</label><br>', html)
        self.assertIn('Nazwa<br>', html)
        self.assertIn('<input name="nazwa">', html)
        self.assertIn('<input type="submit" value="Dodaj">', html)


class LogowanieWylogowanieTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_logowanie(self):
        url = reverse('program:logowanie')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'program/logowanie.html')
        self.assertIn('form', response.context)

    def test_wylogowanie(self):
        url = reverse('program:wylogowanie')
        self.client.force_login(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('program:index'))

class RodzajLiniiTest(TestCase):

    def test_komentarz(self):
        linia = "/* This is a comment */"
        result = rodzaj_linii(linia)
        self.assertEqual(result, "komentarz")

    def test_dyrektywa(self):
        linia = "#include <stdio.h>"
        result = rodzaj_linii(linia)
        self.assertEqual(result, "dyrektywa")

    def test_deklaracja(self):
        linia = "int x;"
        result = rodzaj_linii(linia)
        self.assertEqual(result, "deklaracja")

    def test_procedura(self):
        linia = "void foo() {"
        result = rodzaj_linii(linia)
        self.assertEqual(result, "procedura")

class StworzKatalogTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('program:stworz_katalog')

    def test_stworz_katalog_authenticated(self):
        # Utwórz użytkownika i zaloguj się
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Dane do przesłania
        data = {'nazwa': 'Testowy katalog', 'rodzic': '1'}

        # Wyślij żądanie POST
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        # Sprawdź kod odpowiedzi
        self.assertEqual(response.status_code, 200)

        # Sprawdź odpowiedź JSON
        response_data = json.loads(response.content)
        self.assertEqual(response_data['nazwa'], 'Testowy katalog')

    def test_stworz_katalog_unauthenticated(self):
        # Dane do przesłania
        data = {'nazwa': 'Testowy katalog', 'rodzic': '1'}

        # Wyślij żądanie POST
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        # Sprawdź kod odpowiedzi
        self.assertEqual(response.status_code, 200)

        # Sprawdź odpowiedź JSON
        response_data = json.loads(response.content)
        self.assertEqual(response_data['nazwa'], 'Testowy katalog')


class IndexTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('program:index')

    def test_index_authenticated(self):
        # Utwórz użytkownika i zaloguj się
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Utwórz katalogi i pliki dla zalogowanego użytkownika
        katalog = Katalog.objects.create(nazwa='Katalog 1', rodzic=0, znacznik_dostepnosci=1, wlasciciel=user)
        plik = Plik.objects.create(nazwa='Plik 1', rodzic=0, znacznik_dostepnosci=1, wlasciciel=user)

        # Wyślij żądanie GET
        response = self.client.get(self.url)

        # Sprawdź kod odpowiedzi
        self.assertEqual(response.status_code, 200)

        # Sprawdź, czy odpowiednie dane są dostępne w kontekście
        context = response.context
        self.assertEqual(context['niezalogowany'], False)
        self.assertEqual(list(context['katalogi']), [katalog])
        self.assertEqual(list(context['pliki']), [plik])

    def test_index_unauthenticated(self):
        # Wyślij żądanie GET
        response = self.client.get(self.url)

        # Sprawdź kod odpowiedzi
        self.assertEqual(response.status_code, 200)

        # Sprawdź, czy odpowiednie dane są dostępne w kontekście
        context = response.context
        self.assertEqual(context['niezalogowany'], True)
        self.assertEqual(list(context['katalogi']), [])
        self.assertEqual(list(context['pliki']), [])
class LoginViewTest(TestCase):
    def setUp(self):
        self.url = reverse('program:login')  # Zmień 'login_view' na odpowiedni adres URL widoku

        # Tworzenie użytkownika testowego
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    # def test_login_success(self):
        # Dane do logowania
        data = {
            'username': self.username,
            'password': self.password
        }

        # Wysyłanie żądania POST z danymi logowania
        response = self.client.post(self.url, data)

        # Sprawdzenie, czy użytkownik został pomyślnie zalogowany
        self.assertEqual(response.status_code, 302)  # Oczekiwany kod statusu przekierowania
        # self.assertRedirects(response, reverse('program:index'))  # Oczekiwany adres URL przekierowania

        # Sprawdzenie, czy użytkownik jest zalogowany
        user = authenticate(username=self.username, password=self.password)
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

    def test_login_invalid_credentials(self):
        # Dane do logowania z nieprawidłowymi danymi
        data = {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        }

        # Wysyłanie żądania POST z nieprawidłowymi danymi logowania
        response = self.client.post(self.url, data)

        # Sprawdzenie, czy logowanie zostało odrzucone
        self.assertEqual(response.status_code, 200)  # Oczekiwany kod statusu OK
        self.assertTemplateUsed(response, 'program/logowanie.html')  # Oczekiwany szablon renderowany

        # Sprawdzenie, czy użytkownik nie jest zalogowany
        user = authenticate(username=data['username'], password=data['password'])
        self.assertIsNone(user)
class PobierzSekcjeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('program:pobierz_sekcje')  # Zmień 'pobierz_sekcje' na odpowiedni adres URL widoku
        self.plik = Plik.objects.create()  # Utwórz obiekt Plik
        self.sekcja_1 = Sekcja_pliku.objects.create(id_ojca_pliku=1, opcjonalna_nazwa='Sekcja 1')
        self.sekcja_2 = Sekcja_pliku.objects.create(id_ojca_pliku=1, opcjonalna_nazwa='Sekcja 2')

    def test_pobierz_sekcje(self):
        # Tworzenie żądania GET z odpowiednimi danymi
        request = self.factory.get(self.url, {'plik': self.plik.id})
        
        # Wywołanie widoku
        response = pobierz_sekcje(request)

        # Sprawdzenie poprawności odpowiedzi
        self.assertEqual(response.status_code, 200)  # Oczekiwany kod statusu OK
        self.assertIsInstance(response, JsonResponse)  # Oczekiwany typ odpowiedzi JsonResponse

        # Sprawdzenie zawartości JSON
        json_data = json.loads(response.content)
        self.assertIn('html', json_data)  # Czy zawiera klucz 'html'?
        self.assertIn('zawartosc', json_data)  # Czy zawiera klucz 'zawartosc'?

        # Sprawdzenie zawartości 'html'
        html = json_data['html']

        self.assertIn('<input type="submit" value="Usun">', html)  # Czy zawiera odpowiedni przycisk Usun?

        # Sprawdzenie zawartości 'zawartosc'
        zawartosc = json_data['zawartosc']
        self.assertEqual(zawartosc, 'BRAK') 
class UsunSekcjeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('program:usun_sekcje')  # Zmień 'usun_sekcje' na odpowiedni adres URL widoku

        # Tworzenie testowych obiektów Sekcja_pliku i Plik
        self.plik = Plik.objects.create()
        self.sekcja = Sekcja_pliku.objects.create(id_ojca_pliku=1)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_usun_sekcje(self):
        # Przygotowanie danych żądania POST
        data = {
            'sekcja': self.sekcja.id
        }
        
        # Logowanie użytkownika
        self.client.login(username='testuser', password='testpassword')

        # Tworzenie żądania POST
        request = self.factory.post(self.url, data)
        request.user = self.user
        
 
        response = usun_sekcje(request)

        self.assertEqual(response.status_code, 200)  
        self.assertIsInstance(response, JsonResponse)  
        
        json_data = json.loads(response.content)
        self.assertIn('nazwa', json_data)  
        
        self.assertRaises(Sekcja_pliku.DoesNotExist, Sekcja_pliku.objects.get, id=self.sekcja.id)  
        plik_do_zmiany = Plik.objects.get(id=self.plik.id)  
        # self.assertEqual(plik_do_zmiany.data_ostatniej_zmiany_zawartosci, timezone.now().date())  
        self.assertIn(plik_do_zmiany.opcjonalny_opis, json_data['nazwa']) 
class UsunKatalogViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('program:usun_katalog')

        self.katalog = Katalog.objects.create()

        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_usun_katalog(self):
        data = {
            'rodzic': self.katalog.id
        }

        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)  
        self.assertIsInstance(response, JsonResponse)  

        json_data = response.json()
        self.assertIn('nazwa', json_data) 


        if self.katalog.rodzic:
            rodzic = Katalog.objects.get(id=self.katalog.rodzic.id)  
            self.assertEqual(rodzic.data_ostatniej_zmiany_zawartosci.date(), timezone.now().date())
class FragmentTest(TestCase):
    def test_asm_split(self):

        content = "This is a test.\nNo sections in this content."
        expected_output = "This is a test.\nNo sections in this content.\n"
        assert wypisz_fragment(content) == expected_output
    
 
        content = ";--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\nSection 1\n"
        expected_output = "<div class='asm-section'><div class='asm-section-header' id='header_0'>;--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\n</div><div class='asm-tresc show' id ='tresc_0'>Section 1\n</div></div>\n"
        assert wypisz_fragment(content).strip() == expected_output.strip()

        content = ";--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\nSection 1\n"
        content += ";--------------------------------------------------------\nHeader2\n;--------------------------------------------------------\nSection 2\n"
        expected_output = "<div class='asm-section'><div class='asm-section-header' id='header_0'>;--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\n</div><div class='asm-tresc show' id ='tresc_0'>Section 1\n</div></div>"
        expected_output += "<div class='asm-section'><div class='asm-section-header' id='header_1'>;--------------------------------------------------------\nHeader2\n;--------------------------------------------------------\n</div><div class='asm-tresc show' id ='tresc_1'>Section 2\n</div></div>\n"
        assert wypisz_fragment(content).strip() == expected_output.strip()
    

        content = ""
        expected_output = ""
        assert wypisz_fragment(content) == expected_output
    

        content = ";--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\n;--------------------------------------------------------\nHeader2\n;--------------------------------------------------------\n"
        expected_output = "<div class='asm-section'><div class='asm-section-header' id='header_0'>;--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\n</div><div class='asm-tresc show' id ='tresc_0'></div></div>"
        expected_output += "<div class='asm-section'><div class='asm-section-header' id='header_1'>;--------------------------------------------------------\nHeader2\n;--------------------------------------------------------\n</div><div class='asm-tresc show' id ='tresc_1'></div></div>\n"
        assert wypisz_fragment(content).strip() == expected_output.strip()

class PobierzNiezaleznePlikiTestCase(TestCase):
    def setUp(self):
        # Utwórz instancję klasy RequestFactory
        self.factory = RequestFactory()

        # Utwórz użytkownika testowego
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Utwórz przykładowe pliki
        self.plik1 = Plik.objects.create(nazwa='plik1.txt', rodzic=0, znacznik_dostepnosci=1, wlasciciel=self.user)
        self.plik2 = Plik.objects.create(nazwa='plik2.txt', rodzic=0, znacznik_dostepnosci=1, wlasciciel=self.user)
        self.plik3 = Plik.objects.create(nazwa='plik3.txt', rodzic=0, znacznik_dostepnosci=1, wlasciciel=self.user)

    def test_pobierz_niezalezne_pliki(self):
        # Utwórz żądanie HTTP GET
        request = self.factory.get('/url/')

        # Zaloguj użytkownika w żądaniu
        request.user = self.user

        # Wywołaj funkcję widoku
        response = pobierz_niezalezne_pliki(request)

        # Sprawdź, czy odpowiedź ma status HTTP 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Sprawdź, czy odpowiedź zawiera oczekiwane dane w formacie JSON
        expected_data = {
            'html': f'<li><a href="http://127.0.0.1:8000/{self.plik1.id}">plik1.txt</a></li>'
                     f'<li><a href="http://127.0.0.1:8000/{self.plik2.id}">plik2.txt</a></li>'
                     f'<li><a href="http://127.0.0.1:8000/{self.plik3.id}">plik3.txt</a></li>'
        }
        self.assertJSONEqual(response.content, expected_data)

class Podziel_Sekcje(TestCase):
        # self.factory = RequestFactory()
        # self.folder = Folder.objects.create(name='Test Folder')
        # file = open('./test_error.c', 'r')
        # self.file_error = file.read()
        # file.close()
        # file = open('./test_error.c', 'r')
        # self.file_compile = file.read()
        # file.close()
        # self.file = File.objects.create(name='Test File', parent=self.folder, content=self.file_compile)
        # self.file_error = File.objects.create(name='Test File', parent=self.folder, content=self.file_error)
        # self.client = Client()
    
    def setUp(self):    # self.user = User.objects.create_user(username='your_username', password='your_password')
        Rodzaj_sekcji.objects.create(nazwa='procedura')
        Rodzaj_sekcji.objects.create(nazwa='dyrektywa')
        Rodzaj_sekcji.objects.create(nazwa='deklaracja')
        Rodzaj_sekcji.objects.create(nazwa='assembler')
        Rodzaj_sekcji.objects.create(nazwa='komentarz')
    def test_divide_into_sections(self):
        # Test case 1: No sections in the file
        content = "This is a test.\nNo sections in this file."
        file = Plik(tresc=content, nazwa="test_file")
        file.save()
        podziel(file.tresc, file.id)
        file_sections = Sekcja_pliku.objects.filter(id_ojca_pliku=file.id)
        self.assertEqual(len(file_sections),1)
        self.assertEqual(file_sections[0].poczatek_sekcji,1)
        self.assertEqual(file_sections[0].koniec_sekcji,2)
        self.assertEqual(file_sections[0].rodzaj_sekcji,1)
        # self.assertEqual(file_sections[0].tresc,"This is a test.No sections in this file.")

        # Test case 2: Multiple sections in the file
        content = "int x = 10;\n/* Comment 1 */\nvoid foo() {\n/* Comment 2 */\n}\n/* Comment 3\n Comment 3 */\n  __asm\n  {\n    nop\n  }\n __endasm;\n void bar() {\n   \n}\n"
        file = Plik(tresc=content, nazwa="test_file")
        file.save()
        podziel(file.tresc, file.id)
        file_sections = Sekcja_pliku.objects.filter(id_ojca_pliku = file.id)
        self.assertEqual(len(file_sections),8)

        self.assertEqual(file_sections[0].poczatek_sekcji,1)
        self.assertEqual(file_sections[0].koniec_sekcji,1)
        self.assertEqual(file_sections[0].rodzaj_sekcji,3)
        self.assertEqual(file_sections[0].tresc,"int x = 10;")

        self.assertEqual(file_sections[1].poczatek_sekcji,2)
        self.assertEqual(file_sections[1].koniec_sekcji,2)
        self.assertEqual(file_sections[1].rodzaj_sekcji,3)
        self.assertEqual(file_sections[1].tresc,"/* Comment 1 */")

        self.assertEqual(file_sections[2].poczatek_sekcji, 3)
        self.assertEqual(file_sections[2].koniec_sekcji, 3)
        self.assertEqual(file_sections[2].rodzaj_sekcji,1)
        self.assertEqual(file_sections[2].tresc,"void foo() {")

        self.assertEqual(file_sections[3].poczatek_sekcji,4)
        self.assertEqual(file_sections[3].koniec_sekcji, 4)
        self.assertEqual(file_sections[3].rodzaj_sekcji,3)
        self.assertEqual(file_sections[3].tresc,"/* Comment 2 */")

        self.assertEqual(file_sections[4].poczatek_sekcji,5)
        self.assertEqual(file_sections[4].koniec_sekcji, 5)
        self.assertEqual(file_sections[4].rodzaj_sekcji,1)
        self.assertEqual(file_sections[4].tresc,"}")

        self.assertEqual(file_sections[5].poczatek_sekcji, 6)
        self.assertEqual(file_sections[5].koniec_sekcji,7)
        self.assertEqual(file_sections[5].rodzaj_sekcji,1)
        self.assertEqual(file_sections[5].tresc,"/* Comment 3 Comment 3 */\n")

        self.assertEqual(file_sections[6].poczatek_sekcji,8)
        self.assertEqual(file_sections[6].koniec_sekcji,12)
        self.assertEqual(file_sections[6].rodzaj_sekcji,1)
        self.assertEqual(file_sections[6].tresc,"  __asm  {\n    nop\n  }\n __endasm;\n")

        self.assertEqual(file_sections[7].poczatek_sekcji, 13)
        self.assertEqual(file_sections[7].koniec_sekcji,15)
        self.assertEqual(file_sections[7].rodzaj_sekcji, 1)

        self.assertEqual(file_sections[7].tresc," void bar() {\n}\n")

class StworzPlikTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Rodzaj_sekcji.objects.create(nazwa='procedura')
        Rodzaj_sekcji.objects.create(nazwa='dyrektywa')
        Rodzaj_sekcji.objects.create(nazwa='deklaracja')
        Rodzaj_sekcji.objects.create(nazwa='assembler')
        Rodzaj_sekcji.objects.create(nazwa='komentarz')

    def test_stworz_plik(self):
        request = self.factory.post('/stworz-plik/')
        request.user = self.user
        request.POST = request.POST.copy()  
        request.POST['csrfmiddlewaretoken'] = 'dummytoken'
        request.POST['rodzic'] = '1'

        # Utwórz przykładowy plik
        file_content = 'Example file content'
        uploaded_file = SimpleUploadedFile('example.txt', file_content.encode('utf-8'))
        request.FILES['nazwa'] = uploaded_file

        response = stworz_plik(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Plik.objects.count(), 1)

        plik = Plik.objects.first()
        self.assertEqual(plik.nazwa, 'example.txt')
        self.assertEqual(plik.rodzic, 1)
        self.assertEqual(plik.tresc, file_content)
        self.assertEqual(plik.wlasciciel, self.user)

        # Sprawdź podział pliku na sekcje
        sekcje = Sekcja_pliku.objects.filter(id_ojca_pliku=plik.id)
        self.assertEqual(sekcje.count(), 1)

        sekcja = sekcje.first()
        self.assertEqual(sekcja.opcjonalna_nazwa, f'Plik id: procedura linie: 1-1')
        self.assertEqual(sekcja.tresc, file_content)
        self.assertEqual(sekcja.poczatek_sekcji, 1)
        self.assertEqual(sekcja.koniec_sekcji, 1)
        self.assertEqual(sekcja.id_ojca_pliku, plik.id)

class UsunPlikTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.plik = Plik.objects.create(nazwa='test_file', znacznik_dostepnosci=1)
        setValue(standard_='standard', optymalizacje_='optymalizacje', procesor_='procesor', zalezne_='zalezne', plik_=self.plik.id)

    def test_usun_plik_valid_request(self):
        request = self.factory.post('/usun_plik/')
        request.user = User.objects.create(username='test_user', password='testpassword')
        response = usun_plik(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'nazwa': 'sukces'})
        self.plik.refresh_from_db()
        self.assertEqual(self.plik.znacznik_dostepnosci, 0)
        self.assertIsNotNone(self.plik.data_zmiany_znacznika)

    def test_usun_plik_invalid_json(self):
        request = self.factory.get('/usun_plik/')
        response = usun_plik(request)

        self.assertEqual(response.status_code, 200)
        # self.assertJSONEqual(str(response.content, encoding='utf-8'), {'error': 'Invalid JSON format.'})

    def test_usun_plik_invalid_method(self):
        request = self.factory.get('/usun_plik/')
        response = usun_plik(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'error': 'Invalid request method.'})

class KompilujTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.plik = Plik.objects.create(nazwa='test.c', tresc='Example file content')
        self.plik.save()

    def test_kompiluj(self):
        setValue(standard_='standard', optymalizacje_='optymalizacje', procesor_='procesor', zalezne_='zalezne', plik_=self.plik.id)

        # Utwórz żądanie POST
        url = reverse('program:kompiluj')
        request = self.factory.post(url)
        request.user = self.user
        request.method = 'POST'
        request.POST = request.POST.copy()
        # request.POST['plik'] = self.plik.id

        response = kompiluj(request)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('stdout', response_data)
        self.assertIn('stderr', response_data)
        self.assertIn('status', response_data)

class PobierzKatalogiTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.katalog = Katalog.objects.create(nazwa='test_katalog', rodzic=0, znacznik_dostepnosci=True, wlasciciel=self.user)
        self.podkatalog = Katalog.objects.create(nazwa='test_podkatalog', rodzic=self.katalog.id, znacznik_dostepnosci=True, wlasciciel=self.user)
        self.plik = Plik.objects.create(nazwa='test_plik', rodzic=self.katalog.id, znacznik_dostepnosci=True)

    def test_pobierz_katalogi_authenticated_user(self):
        request = self.factory.get('/pobierz_katalogi/')
        request.user = self.user
        response = pobierz_katalogi(request)

        expected_data = [
            {
                'id': self.katalog.id,
                'nazwa': 'test_katalog',
                'podkatalogi': [
                    {
                        'id': self.podkatalog.id,
                        'nazwa': 'test_podkatalog',
                        'podkatalogi': [],  # Dodajemy puste podkatalogi dla testu
                        'podpliki': []  # Dodajemy puste podpliki dla testu
                    }
                ],
                'podpliki': [
                    {
                        'id': self.plik.id,
                        'nazwa': 'test_plik'
                    }
                ]
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), expected_data)
from django.shortcuts import render
# from program.forms import standardForm, procesorForm, optymalizacjeForm
from program.models import Katalog, Plik, Sekcja_pliku, Rodzaj_sekcji
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import subprocess
import re
import os
import json
from .forms import LoginForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('program:index'))
    form = LoginForm()
    context = {
        'form': form  # Dodaj formularz do kontekstu
    }
    return render(request, 'program/logowanie.html', context)

standard = ''
optymalizacje = ''
procesor = ''
zalezne = ''
plik = 0
zmiana = False
bledy = []
zmienna = 0


def setValue(standard_, optymalizacje_, procesor_, zalezne_, plik_):
    global standard
    global optymalizacje
    global standard
    global plik
    global zalezne
    standard = standard_
    optymalizacje = optymalizacje_
    procesor = procesor_
    zalezne = zalezne_
    plik = plik_
    
    
def wypisz_fragment(tekst):
    pierwsza_linia = 1
    tekst = tekst.splitlines()
    wynik = ""
    index = 0 
    for linia in tekst:
        if linia == ";--------------------------------------------------------":
            if pierwsza_linia:
                if wynik != "":
                    wynik += "</div></div>"
                    index = index  + 1
                wynik += "<div class='asm-section'>"
                wynik += "<div class='asm-section-header' id='header_" +str(index) + "'>"
                wynik += linia + '\n'
                pierwsza_linia = 0
            else:
                wynik += linia + '\n'
                wynik += "</div><div class='asm-tresc show' id ='tresc_" + str(index) + "'>"
                pierwsza_linia = 1
        else:
            wynik += linia + '\n'
    if "<div" in wynik:
        return wynik + "</div></div>"
    else:
        return wynik

def index(request, id_pliku=None):
    if request.user.is_authenticated:
        katalogi = Katalog.objects.filter(rodzic = 0, znacznik_dostepnosci =1, wlasciciel = request.user)
        pliki = Plik.objects.filter(rodzic = 0, znacznik_dostepnosci = 1, wlasciciel = request.user)
        niezalogowany = False
        # """SELECT id, nazwa from program_plik where rodzic = 0 and znacznik_dostepnosci = 1""")
    else:
        katalogi = ''
        pliki = ''
        niezalogowany = True
    global plik
    global zmiana 
    global bledy
    zmiana = False
    if id_pliku == None:
        # id_pliku = plik
        # print("siema")
        id_pliku = 0
        plik = 0
    else :
        if plik != id_pliku:
            zmiana = True
            bledy = []
        # print(id_pliku)
        plik = id_pliku
    global standard
    global optymalizacje
    skompilowany = 0
    lista = ''
    # print(id_pliku)
    if(id_pliku!=None and id_pliku!=0):
        # print(id_pliku)
        plik_do_wyswietlenia = Plik.objects.get(id=id_pliku)
        # print(plik_do_wyswietlenia.tresc)
        lista = plik_do_wyswietlenia.tresc.encode('utf-8')
        # lista = plik_do_wyswietlenia.tresc.encode('utf-8')
        # print(plik.tresc)
    # pliki = Plik.objects.raw("""SELECT id, nazwa from program_plik where rodzic = 0 and znacznik_dostepnosci = 1""")
    sekcje = Sekcja_pliku.objects.all()
    fragment_kodu = ''
    if len(bledy) > 1 and id_pliku != None and zmiana != True :
        fragment_kodu = 'Blad kompilacji'
        if os.path.isfile(str(id_pliku) + ".asm"):
            os.remove(str(id_pliku) + '.asm')
    else :
        if id_pliku != None and zmiana!= True:
            if os.path.isfile(str(id_pliku) + ".asm"):
                f = open(str(id_pliku) + ".asm", "r")
                fragment_kodu = f.read()
                f.close()
                os.remove(str(id_pliku) + '.asm')
                skompilowany = 1
                f = open("plik.asm","w+")
                f.write(fragment_kodu)
                f.close()
                fragment_kodu = wypisz_fragment(fragment_kodu)

    context = {
        'niezalogowany' : niezalogowany,
        'katalogi' : katalogi,
        'skompilowany' : skompilowany,
        'id_pliku':id_pliku,
        'standard':standard,
        'optymalizacje':optymalizacje,
        'procesor' :procesor,
        'zalezne' :zalezne,
        'pliki' : pliki,
        'sekcje': sekcje,
        'lista' : lista,
        'fragment_kodu': fragment_kodu,
    }
    return render(request, 'program/index.html', context)

def pobierz_katalogi(request):
    def wypisz_katalog(katalog):
        podkatalogi = Katalog.objects.filter(rodzic=katalog.id, znacznik_dostepnosci=True)
        podpliki = Plik.objects.filter(rodzic=katalog.id, znacznik_dostepnosci=True)
        dane = {
            'id': katalog.id,
            'nazwa': katalog.nazwa,
            'podkatalogi': [],
            'podpliki': []
        }
        for podkatalog in podkatalogi:
            if podkatalog != katalog:
                dane['podkatalogi'].append(wypisz_katalog(podkatalog))
        for podplik in podpliki:
            dane['podpliki'].append({
                'id': podplik.id,
                'nazwa': podplik.nazwa
            })
        return dane
    if request.user.is_authenticated:
        katalogi = Katalog.objects.filter(rodzic=0, znacznik_dostepnosci=1, wlasciciel=request.user)
    else :
        katalogi =''
    dane = []
    for katalog in katalogi:
        dane.append(wypisz_katalog(katalog))
    # print(dane)
    return JsonResponse(dane, safe=False)

def pobierz_niezalezne_pliki(request):
    if request.user.is_authenticated:
        pliki = Plik.objects.filter(rodzic=0, znacznik_dostepnosci=1, wlasciciel=request.user)
    else:
        pliki = ''
    html = ''
    for plik in pliki:
        html += f'<li><a href="http://127.0.0.1:8000/{plik.id}">{plik.nazwa}</a></li>'
    
    return JsonResponse({'html': html})

def pobierz_sekcje(request):
    global plik
    # print(plik)
    sekcje = Sekcja_pliku.objects.filter(id_ojca_pliku = plik)
    # print(sekcje)
    html = ''
    for sekcja in sekcje:
        html += f'<input type="radio" name="sekcja" id="{sekcja.id}" value="{sekcja.id}">'
        html += f'<label for="{sekcja.id}">{sekcja.opcjonalna_nazwa}</label><br>'
    html += '<input type="submit" value="Usun">'
    # html += '<button id="anuluj-button">Anuluj</button>'
    # global plik
    # print(plik)
    if plik > 0 : 
        plik_do_wyswietlenia = Plik.objects.get(id = plik)
        zawartosc = plik_do_wyswietlenia.tresc
    else :
        zawartosc = 'BRAK'
    # zawartosc = plik_do_wyswietlenia.tresc
    # zawartosc.replace('<', '&lt;').replace('>', '&gt;')
    # print(zawartosc)

    # 'zawartosc' : zawartosc.replace('<', '&lt;').replace('>', '&gt;')
    return JsonResponse({'html': html,
        'zawartosc' : zawartosc
    })
    


def stworz_katalog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nazwa = data['nazwa']
            rodzic = data['rodzic']
            if request.user.is_authenticated:
                user = request.user
            else :
                user = None
            nowy_katalog = Katalog.create(nazwa, rodzic, user)
            nowy_katalog.save()  
            odpowiedz = {'nazwa':nazwa}
            return JsonResponse(odpowiedz)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'})
    return JsonResponse({'error': 'Invalid request method.'})

def rodzaj_linii(linia):
    match = re.fullmatch(".*__asm.*", linia)
    if match != None :
        return "assembler"
    match = re.fullmatch("\s*\/\*.*", linia)
    if match != None :
        return "komentarz"
    match = re.fullmatch("\s*#.*", linia)
    if match != None :
        return "dyrektywa"
    match = re.fullmatch("\s*(int|double|float|char).*\;", linia)
    if match != None :
        return "deklaracja"
    return "procedura"

def podziel(tresc, rodzic):
    list = tresc.splitlines()
    tresc_w_sekcji = ""
    aktualny_licznik = 1
    rodzaj_sekcji = ''
    poczatek_sekcji = 1
    for element in list :
        if re.fullmatch("\s*", element) != None:
            aktualny_licznik = aktualny_licznik + 1
            tresc_w_sekcji += '\n'
            continue
        # rodzaj = rodzaj_linii(element)
        if rodzaj_sekcji == "komentarz" and re.fullmatch(".*\*\/*", element) == None:
            aktualny_licznik = aktualny_licznik + 1
            tresc_w_sekcji = tresc_w_sekcji +element + '\n'
            continue
        if rodzaj_sekcji== "komentarz" and re.fullmatch(".*\*\/*", element) != None:
            tresc_w_sekcji += element + '\n'
            aktualny_licznik = aktualny_licznik + 1
            nazwa = 'Plik id: '+ 'komentarz' + ' linie: '+str(poczatek_sekcji)+'-'+str(aktualny_licznik-1)
            nowa_sekcja = Sekcja_pliku.create(nazwa, 
            "komentarz", tresc_w_sekcji, poczatek_sekcji, aktualny_licznik -1, nowy_rodzaj.id, rodzic)
            # begin = first_line, end = counter - 1, type = section_type,  file = file, content=section_content)
            # nowa_sekcja.name = 'Plik id: '+ str(nowy_rodzaj.nazwa) + ' linie: '+str(poczatek_sekcji)+'-'+str(aktualny_licznik-1)
            nowa_sekcja.save()
            rodzaj_sekcji = ''
            tresc_w_sekcji = ""
            poczatek_sekcji = aktualny_licznik
            continue
        if rodzaj_sekcji == "assembler" and re.fullmatch(".*__endasm;.*", element) == None:
            aktualny_licznik = aktualny_licznik + 1
            tresc_w_sekcji = tresc_w_sekcji +element + '\n'
            continue
        if rodzaj_sekcji == "assembler" and re.fullmatch(".*__endasm;.*", element) != None:
            tresc_w_sekcji += element + '\n'
            aktualny_licznik = aktualny_licznik + 1
            nowa_sekcja = Sekcja_pliku.create('Plik id: '+ 'assembler' + ' linie: '+str(poczatek_sekcji)+'-'+str(aktualny_licznik-1), 
            'assembler', tresc_w_sekcji, poczatek_sekcji, aktualny_licznik -1, nowy_rodzaj.id, rodzic)
            # begin = first_line, end = counter - 1, type = section_type,  file = file, content=section_content)
            # nowa_sekcja.name = 'Plik id: '+ str(nowy_rodzaj.nazwa) + ' linie: '+str(poczatek_sekcji)+'-'+str(aktualny_licznik-1)
            nowa_sekcja.save()
            rodzaj_sekcji = ''
            tresc_w_sekcji = ""
            poczatek_sekcji = aktualny_licznik
            continue
        rodzaj = rodzaj_linii(element)
        if rodzaj == "komentarz" and re.fullmatch(".*\*\/\s*", element):
            if rodzaj_sekcji != '' :
                nowy_rodzaj = Rodzaj_sekcji.objects.get(nazwa = rodzaj_sekcji)
                nazwa = 'Plik id ' + nowy_rodzaj.nazwa + ' linie ' + str(poczatek_sekcji)+'-'+str(aktualny_licznik-1)
                nowa_sekcja = Sekcja_pliku.create(nazwa, nowy_rodzaj.nazwa, tresc_w_sekcji, poczatek_sekcji, aktualny_licznik -1, nowy_rodzaj.id,rodzic)
                nowa_sekcja.save()
                # nowa_sekcja = Sekcja_pliku.create(begin = first_line, end = counter - 1, type = section_type,  file = file, content=section_content)
                # nowa_sekcja.name = 'File id: '+ str(file.id) + ' lines: '+str(first_line)+'-'+str(counter-1)
                # nowa_sekcja.save()
            # section_type = actual_line_type
            nowy_rodzaj = Rodzaj_sekcji.objects.get(nazwa = rodzaj_sekcji)
            tresc_w_sekcji = tresc_w_sekcji + '\n'
            # poczatek_sekcji = aktualny_licznik
            aktualny_licznik = aktualny_licznik + 1
            nazwa = 'Plik id ' + "komentarz" + ' linie ' + str(poczatek_sekcji)+'-'+str(aktualny_licznik-1)
            nowa_sekcja = Sekcja_pliku.create(nazwa, nowy_rodzaj.nazwa, element, poczatek_sekcji + 1, aktualny_licznik -1, 3,rodzic)
            nowa_sekcja.save()
            # aktualny_licznik = aktualny_licznik + 1
            rodzaj_sekcji = ''
            tresc_w_sekcji = ""
            poczatek_sekcji = aktualny_licznik
            continue
        # if(element == '\n')
        if rodzaj == rodzaj_sekcji :
            tresc_w_sekcji+= element + '\n'
        else :
            if aktualny_licznik > 1 and rodzaj_sekcji != '' :
                nowy_rodzaj = Rodzaj_sekcji.objects.get(nazwa = rodzaj_sekcji)
                nazwa = 'Plik id: '+ nowy_rodzaj.nazwa + ' linie: '+str(poczatek_sekcji)+'-'+str(aktualny_licznik-1)
                nowa_sekcja = Sekcja_pliku.create(nazwa,nowy_rodzaj.nazwa,tresc_w_sekcji,poczatek_sekcji, aktualny_licznik - 1, nowy_rodzaj.id, rodzic)
                nowa_sekcja.save()
                rodzaj_sekcji = rodzaj
                tresc_w_sekcji = element
                poczatek_sekcji = aktualny_licznik
            else :
                rodzaj_sekcji = rodzaj
                tresc_w_sekcji = element
                poczatek_sekcji = aktualny_licznik
        aktualny_licznik = aktualny_licznik + 1
    # print('\n')
    # print('('+rodzaj_sekcji+')')
    nowy_rodzaj = Rodzaj_sekcji.objects.get(nazwa = rodzaj_sekcji)
    nazwa = 'Plik id: '+ nowy_rodzaj.nazwa + ' linie: '+str(poczatek_sekcji)+'-'+str(aktualny_licznik-1)
    nowa_sekcja = Sekcja_pliku.create(nazwa,nowy_rodzaj.nazwa,tresc_w_sekcji,poczatek_sekcji, aktualny_licznik - 1, nowy_rodzaj.id, rodzic)
    nowa_sekcja.save()
def stworz_plik(request):
    if request.method == 'POST':
        # Odczytaj wartość CSRF tokena
        csrf_token = request.POST.get('csrfmiddlewaretoken', '')

        # Odczytaj wartości innych pól formularza
        rodzic = request.POST.get('rodzic', '')
        # ... odczytaj inne pola formularza

        # Odczytaj przesłany plik
        plik = request.FILES['nazwa']
        nazwa_pliku = plik.name
        zawartosc_pliku = plik.read().decode('utf-8')  
        # print(zawartosc_pliku)
        # print("pauza")
        if request.user.is_authenticated:
            user = request.user
        else :
            user = None
        # print(tresc)
        nowy_plik = Plik.create(nazwa_pliku, rodzic, zawartosc_pliku,user)
        nowy_plik.save()
        podziel(zawartosc_pliku, nowy_plik.id)  

        # Przetwórz dane, wykonaj odpowiednie operacje

        # Zwróć odpowiedź
        odpowiedz = {'status': 'success'}
        return JsonResponse(odpowiedz)

    return JsonResponse({'error': 'Invalid request method.'})
# def stworz_plik(request):
#     print("jestem")
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             nazwa = data['nazwa']
#             print(nazwa)
#             rodzic = data['rodzic']
#             print(rodzic)
#             # if request.user.is_authenticated:
#             #     user = request.user
#             # else :
#             #     user = None
#             # nowy_katalog = Katalog.create(nazwa, rodzic, user)
#             # nowy_katalog.save()  
#             odpowiedz = {'nazwa':"raz"}
#             return JsonResponse(odpowiedz)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format.'})
#     return JsonResponse({'error': 'Invalid request method.'})

    # plik = request.FILES['nazwa']
    # rodzic = int(request.POST["rodzic"])
    # tresc = plik.read().decode("utf-8")
    # if request.user.is_authenticated:
    #     user = request.user
    # else :
    #     user = None
    # nowy_plik = Plik.create(plik.name, rodzic, tresc,user)
    # nowy_plik.save() 
    # podziel(tresc, nowy_plik.id) 
    # return HttpResponseRedirect(reverse('program:index'))

# def usuwanie_katalogu(request):
#     katalogi = Katalog.objects.filter(znacznik_dostepnosci =1 )
#     context = {
#         'katalogi': katalogi,
#     }
#     return render(request, 'program/usuwanie_katalogu.html', context)

def logowanie(request):
    form = LoginForm()
    context = {
        'form': form  
    }
    return render(request, 'program/logowanie.html', context)

def wylogowanie(request):
    global plik
    plik = 0
    logout(request)
    return HttpResponseRedirect(reverse('program:index'))
    
def usun_sekcje(request):
    if request.method == 'POST':
        try:
            sekcja = request.POST.get('sekcja')
            if request.user.is_authenticated:
                user = request.user
            else :
                user = None
            sekcja_do_usuniecia = get_object_or_404(Sekcja_pliku, pk = sekcja)
            id_ojca_pliku = sekcja_do_usuniecia.id_ojca_pliku
            plik_do_zmienienia = get_object_or_404(Plik, pk = id_ojca_pliku)
            plik_do_zmienienia.data_ostatniej_zmiany_zawartosci = timezone.now()
            pomocnicza_tresc = plik_do_zmienienia.tresc
            lista=pomocnicza_tresc.splitlines()
            poczatek = sekcja_do_usuniecia.poczatek_sekcji
            if poczatek != 0:
                poczatek= poczatek - 1 
            koniec = sekcja_do_usuniecia.koniec_sekcji
            tresc = lista[0:poczatek] + lista[koniec:len(lista)]
            ciag_znakow = '\n'.join(tresc)
            plik_do_zmienienia.tresc = ciag_znakow
            plik_do_zmienienia.save()
            sekcje = Sekcja_pliku.objects.filter(id_ojca_pliku = id_ojca_pliku)
            for sekcja_do_zmiany in sekcje:
                if sekcja_do_zmiany.id == sekcja:
                    continue
                if sekcja_do_zmiany.poczatek_sekcji < poczatek:
                    continue
            nowy_poczatek = sekcja_do_zmiany.poczatek_sekcji - (koniec - poczatek)
            nowy_koniec = sekcja_do_zmiany.koniec_sekcji - (koniec - poczatek)
            sekcja_do_zmiany.poczatek_sekcji = nowy_poczatek
            sekcja_do_zmiany.koniec_sekcji = nowy_koniec
            nazwa_sekcji = sekcja_do_zmiany.opcjonalny_opis
            nazwa = 'Plik id: '+ nazwa_sekcji + ' linie: '+str(nowy_poczatek)+'-'+str(nowy_koniec)
            sekcja_do_zmiany.opcjonalna_nazwa = nazwa
            sekcja_do_zmiany.save()
            sekcja_do_usuniecia.delete()
            odpowiedz = {'nazwa':nazwa}
            return JsonResponse(odpowiedz)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'})
    return JsonResponse({'error': 'Invalid request method.'})


def usun_rekurencyjnie(folder):
    pass
    katalogi = Katalog.objects.filter(rodzic = folder.id)
    for element in katalogi:
        usun_rekurencyjnie(element)
    pliki = Plik.objects.filter(rodzic = folder.id)
    for element in pliki:
        element.znacznik_dostepnosci = 0
        element.data_zmiany_znacznika = timezone.now()
        element.save()
    folder.znacznik_dostepnosci = 0
    folder.data_zmiany_znacznika = timezone.now()
    folder.save()

def pobierz_do_usuwania_katalogu(request):
    if request.user.is_authenticated:
        katalogi = Katalog.objects.filter(znacznik_dostepnosci=1, wlasciciel=request.user)
    else:
        katalogi = ''
    html = ''
    for katalog in katalogi:
        html += f'<input type="radio" name="rodzic" id="{katalog.id}" value="{katalog.id}">'
        html += f'<label for="{katalog.id}">{katalog.nazwa}</label><br>'
    html += '<input type="submit" value="Usun">'
    # html += '<button id="anuluj-button">Anuluj</button>'
    
    return JsonResponse({'html': html})
    # print("pppo")
def usun_katalog(request):
    if request.method == 'POST':
        try:
            katalog = request.POST.get('rodzic')
            # print(katalog)
            if request.user.is_authenticated:
                user = request.user
            else :
                user = None
            folder = get_object_or_404(Katalog, pk = katalog)
            id_ojca = folder.rodzic
            if id_ojca > 0:
                katalog_nadrzedny = get_object_or_404(Katalog, pk = id_ojca)
                katalog_nadrzedny.data_ostatniej_zmiany_zawartosci = timezone.now()
                katalog_nadrzedny.save()
            usun_rekurencyjnie(folder)
            odpowiedz = {'nazwa':"sukces"}
            return JsonResponse(odpowiedz)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'})
    return JsonResponse({'error': 'Invalid request method.'})


def usun_plik(request):
    if request.method == 'POST':
        global plik
        # print(plik)
        try:
            # plik = request.POST.get('rodzic')
            # print(katalog)
            if request.user.is_authenticated:
                user = request.user
            else :
                user = None
            # plik = -1
            plik_do_usuniecia = get_object_or_404(Plik, pk = plik)
            plik_do_usuniecia.znacznik_dostepnosci = 0
            plik_do_usuniecia.data_zmiany_znacznika = timezone.now()
            plik_do_usuniecia.save()
            plik = 0
            odpowiedz = {'nazwa':"sukces"}
            return JsonResponse(odpowiedz)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'})
    return JsonResponse({'error': 'Invalid request method.'})

def kompiluj(request):
    global plik
    if request.method == 'POST':
        # print(plik)
        plik_z_trescia = get_object_or_404(Plik, id = plik)
        f = open(str(plik) + '.c', 'w+')
        f.write(plik_z_trescia.tresc)
        f.close()
        command = [settings.SDCC_PATH, '-S']
        command += ['--std-' + standard]
        command += ['-m' + procesor]
        command += optymalizacje
        command += [zalezne]
        command += [f'{plik}.c']
        wynik = subprocess.run(command, capture_output=True)
        os.remove(str(plik) +'.c')
        fragment_kodu = ''
        id_pliku = plik 
        if os.path.isfile(str(id_pliku) + ".asm"):
            f = open(str(id_pliku) + ".asm", "r")
            fragment_kodu = f.read()
            # print(fragment_kodu)
            f.close()
            os.remove(str(id_pliku) + '.asm')
            skompilowany = 1
            f = open("plik.asm","w+")
            f.write(fragment_kodu)
            f.close()
            fragment_kodu = wypisz_fragment(fragment_kodu)
            # print(fragment_kodu)
        odpowiedz = {
        'stdout': fragment_kodu,
        'stderr': wynik.stderr.decode('utf-8'),
        'status': wynik.returncode  
        }
        # print(odpowiedz)
        return JsonResponse(odpowiedz)
    return JsonResponse({'error': 'Invalid request method.'})

def pobierz(request, plik_id):
    nazwa = Plik.objects.get(pk= plik_id).nazwa
    if re.fullmatch(".+\.c", nazwa) != None:
        nazwa = nazwa.replace(".c", "")
    nazwa += '.asm'
    return FileResponse(open("plik.asm", "rb"), as_attachment=True, filename = nazwa) 

def pobierz_do_tworzenia_katalogi(request):
    # print('\n\n\n')
    # print(request.user)
    # print('\n\n\n')
    if request.user.is_authenticated:
        katalogi = Katalog.objects.filter(znacznik_dostepnosci=1, wlasciciel=request.user)
    else:
        katalogi = ''
    html = ''
    for katalog in katalogi:
        html += f'<input type="radio" name="rodzic" id="{katalog.id}" value="{katalog.id}">'
        html += f'<label for="{katalog.id}">{katalog.nazwa}</label><br>'

    html += '<input type="radio" name="rodzic" id="0" value="0">'
    html += '<label for="0" name="rodzic">Niezależny katalog</label><br>'
    html += 'Nazwa<br>'
    html += '<input name="nazwa">'
    html += '<input type="submit" value="Dodaj">'
    # html += '<button id="anuluj-button">Anuluj</button>'
    
    return JsonResponse({'html': html})

def pobierz_do_tworzenia_pliku(request):
    if request.user.is_authenticated:
        katalogi = Katalog.objects.filter(znacznik_dostepnosci=1, wlasciciel=request.user)
    else:
        katalogi = ''
    html = ''
    for katalog in katalogi:
        html += f'<input type="radio" name="rodzic" id="{katalog.id}" value="{katalog.id}">'
        html += f'<label for="{katalog.id}">{katalog.nazwa}</label><br>'

    html += '<input type="radio" name="rodzic" id="0" value="0">'
    html += '<label for="0" name="rodzic">Niezależny katalog</label><br>'
    html += '<input type="file" name="nazwa" accept=".c">'
    html += '<input type="submit" value="Dodaj">'
    # html += '<button id="anuluj-plik">Anuluj</button>'
    
    return JsonResponse({'html': html})

def zmien_zmienna(request):
    if request.method == 'POST':
        global standard
        global procesor
        global optymalizacje
        global zalezne
        try:
            data = json.loads(request.body)
            nazwa = data['nazwa']
            # print(nazwa)
            if nazwa == 'standard':
                standard = data['standard']
                # print(standard)
            if nazwa == 'procesor':
                procesor = data['procesor']
                # print(procesor)
            if nazwa == 'zalezne':
                zalezne = data['zalezne']
            if nazwa == 'optymalizacje':
                # print(data)
                optymalizacje = data['optymalizacje']
                # print(siema)
                # print(optymalizacje)
            odpowiedz = {'nazwa':nazwa}
            # print(nazwa)
            return JsonResponse(odpowiedz)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'})

    return JsonResponse({'error': 'Invalid request method.'})

def zapisz_plik(request):
    if request.method == 'POST':
        try:
            # data = json.loads(request.body)
            # zawartosc = data['zawartosc']
            zawartosc = request.POST.get('zawartosc')
            # plik = Plik.objects.get_object_or_404(id= plik)
            plik_z_zawartoscia = get_object_or_404(Plik, id = plik)
            # plik = Katalog.objects.filter(znacznik_dostepnosci=1, wlasciciel=request.user)
            plik_z_zawartoscia.tresc = zawartosc
            plik_z_zawartoscia.data_ostatniej_zmiany_zawartosci = timezone.now()
            plik_z_zawartoscia.save()
            return JsonResponse({})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'})

    return JsonResponse({'error': 'Invalid request method.'})


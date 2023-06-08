from django.urls import path

from . import views
app_name = 'program'
urlpatterns = [
    path('', views.index, name='index'),
    path('pobierz_sekcje', views.pobierz_sekcje, name='pobierz_sekcje'),
    path('pobierz_do_usuwania_katalogu', views.pobierz_do_usuwania_katalogu, name='pobierz_do_usuwania_katalogu'),
    path('login', views.login_view, name='login'),
    path('usun_katalog', views.usun_katalog, name='usun_katalog'),
    path('usun_plik', views.usun_plik, name='usun_plik'),
    path('usun_sekcje', views.usun_sekcje, name='usun_sekcje'),
    path('stworz_katalog', views.stworz_katalog, name='stworz_katalog'),
    path('stworz_plik', views.stworz_plik, name='stworz_plik'),
    path('logowanie', views.logowanie, name='logowanie'),
    path('wylogowanie', views.wylogowanie, name = 'wylogowanie'),
    # path('zlacz_sekcje', views.zlacz_sekcje, name='zlacz_sekcje'),
    # path('dodaj_sekcje', views.dodaj_sekcje, name='dodaj_sekcje'),
    # path('tworzenie_katalogu', views.tworzenie_katalogu, name = 'tworzenie_katalogu'),
    # path('usuwanie_katalogu', views.usuwanie_katalogu, name = 'usuwanie_katalogu'),
    # path('usuwanie_pliku', views.usuwanie_pliku, name ='usuwanie_pliku'),
    # path('tworzenie_pliku', views.tworzenie_pliku, name ='tworzenie_pliku'),
    # path('wyswietl_kod/<int:id_pliku>', views.wyswietl_kod, name='wyswietl_kod'),
    path('<int:id_pliku>', views.index, name='index'),
    # path('<int:id_pliku>/<int:standard>/<int:optymalizacje>/<int:procesor>/<int:zalezne>', views.index_z_opcjami, name='index_z_opcjami'),
    # path('usuwanie_sekcji', views.usuwanie_sekcji, name ='usuwanie_sekcji'),
    # path('dodaj_standard', views.dodaj_standard, name ='dodaj_standard'),
    # path('dodaj_procesor', views.dodaj_procesor, name ='dodaj_procesor'),
    # path('dodaj_zalezne', views.dodaj_zalezne, name = 'dodaj_zalezne'),
    # path('dodaj_optymalizacje', views.dodaj_optymalizacje, name ='dodaj_optymalizacje'),
    # dodaj_standard(request, id_standardu)
    # path('laczenie_sekcji', views.laczenie_sekcji, name ='laczenie_sekcji'),
    path('kompiluj', views.kompiluj, name ='kompiluj'),
    path('pobierz/<int:plik_id>', views.pobierz, name ='pobierz'),
    path('zmien_zmienna', views.zmien_zmienna, name='zmien_zmienna'),
    path('pobierz_do_tworzenia_pliku', views.pobierz_do_tworzenia_pliku, name='pobierz_do_tworzenia_pliku'),
    path('pobierz_do_tworzenia_katalogi', views.pobierz_do_tworzenia_katalogi, name='pobierz_do_tworzenia_katalogi'),
    path('pobierz_katalogi', views.pobierz_katalogi, name='pobierz_katalogi'),
    path('pobierz_niezalezne_pliki', views.pobierz_niezalezne_pliki, name ='pobierz_niezalezne_pliki'),
    path('zapisz_plik', views.zapisz_plik, name = 'zapisz_plik'),
    # path('tworzenie_sekcji', views.tworzenie_sekcji, name = 'tworzenie_sekcji')
]
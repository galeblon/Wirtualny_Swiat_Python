from Wspolrzedne import *
from random import *
from Zwierze import *
from Zwierzeta.Wilk import Wilk
from Zwierzeta.Owca import Owca
from Zwierzeta.Zolw import Zolw
from Zwierzeta.Lis import Lis
from Zwierzeta.Antylopa import Antylopa
from Rosliny.Trawa import Trawa
from Rosliny.Mlecz import Mlecz
from Rosliny.Guarana import Guarana
from Rosliny.WilczeJagody import WilczeJagody
from Rosliny.BarszczSosnowskiego import BarszczSosnowskiego
from Zwierzeta.Czlowiek import Czlowiek
from shapely import geometry
from tkinter import StringVar


class Swiat:
    def __init__(self, wysokosc, szerokosc):
        self.wysokosc = wysokosc
        self.szerokosc = szerokosc
        self.polecenie = None
        self.__lista_organizmow = []
        self.__lista_komunikatow = []
        self.__lista_pol = []
        self.__plansza = [[None for x in range(szerokosc)] for y in range(wysokosc)]

    def rysuj_swiat(self, obraz):
        rozmiar_kraty = min(obraz.winfo_height()/self.wysokosc, obraz.winfo_width()/self.szerokosc)
        self.__lista_pol.clear()
        for y in range(self.wysokosc):
            for x in range(self.szerokosc):
                kolor = 'saddle brown'
                nazwa = ''
                if self.__plansza[y][x] is not None and self.__plansza[y][x].czy_zyje():
                    kolor, nazwa = self.__plansza[y][x].rysowanie(obraz)
                    nazwa = str(self.__lista_organizmow.index(self.__plansza[y][x])) + nazwa
                self.__lista_pol.append(obraz.create_rectangle(x*rozmiar_kraty, y*rozmiar_kraty, (x+1)*rozmiar_kraty,
                                       (y+1)*rozmiar_kraty, fill=kolor))
                if int(rozmiar_kraty // 6) > 1:
                    obraz.create_text((x + 0.5) * rozmiar_kraty, (y + 0.4) * rozmiar_kraty, fill='black',
                                      font=('Helvetica', int(rozmiar_kraty // 7)),
                                      text=nazwa, width=rozmiar_kraty)
                if self.__plansza[y][x] is not None \
                        and int(rozmiar_kraty // 7) > 1 \
                        and isinstance(self.__plansza[y][x], Zwierze) is True \
                        and not self.__plansza[y][x].czy_dorosly() \
                        and self.__plansza[y][x].czy_zyje():
                    obraz.create_text((x + 0.5) * rozmiar_kraty, (y + 0.7) * rozmiar_kraty, fill='black',
                                      font=('Helvetica', int(rozmiar_kraty // 7)), text='dziecko', width=rozmiar_kraty)

    def znajdz_wolne_sasiadujace(self, pozycja):
        nowe = Wspolrzedne(pozycja.get_x(), pozycja.get_y())
        poprawne_pola = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                nowe.set_xy(pozycja.get_x()+x, pozycja.get_y()+y)
                if self.czy_punkt_nalezy(nowe) and (self.znajdz_organizm(nowe) is None
                                                    or not self.znajdz_organizm(nowe).czy_zyje()):
                    poprawne_pola.append(Wspolrzedne(nowe.get_x(), nowe.get_y()))
        if len(poprawne_pola) != 0:
            return poprawne_pola[randint(0, len(poprawne_pola)-1)]
        return None

    def znajdz_sasiadujace(self, pozycja):
        nowe = Wspolrzedne(pozycja.get_x(), pozycja.get_y())
        poprawne_pola = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                nowe.set_xy(pozycja.get_x()+x, pozycja.get_y()+y)
                if self.czy_punkt_nalezy(nowe) and nowe != pozycja:
                    poprawne_pola.append(Wspolrzedne(nowe.get_x(), nowe.get_y()))
        if len(poprawne_pola) != 0:
            return poprawne_pola[randint(0, len(poprawne_pola)-1)]
        return None

    def znajdz_sasiadujace_pola(self, pozycja):
        nowe = Wspolrzedne(pozycja.get_x(), pozycja.get_y())
        poprawne_pola = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                nowe.set_xy(pozycja.get_x() + x, pozycja.get_y() + y)
                if self.czy_punkt_nalezy(nowe) and nowe != pozycja:
                    poprawne_pola.append(Wspolrzedne(nowe.get_x(), nowe.get_y()))
        if len(poprawne_pola) != 0:
            return poprawne_pola
        return None

    def znajdz_sasiadujace_klawisz(self, pozycja, kierunek):
        ruchy = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0),
            "e": (1, -1),
            "q": (-1, -1),
            "z": (-1, 1),
            "c": (1, 1),
        }
        try:
            x, y = ruchy[kierunek]
        except KeyError:
            x = 0
            y = 0
        nowe = Wspolrzedne(pozycja.get_x()+x, pozycja.get_y()+y)
        if self.czy_punkt_nalezy(nowe) and nowe != pozycja:
            return nowe
        return None

    def czy_punkt_nalezy(self, punkt):
        if 0 < punkt.get_x() <= self.szerokosc:
            if 0 < punkt.get_y() <= self.wysokosc:
                return True
        return False

    def znajdz_organizm(self, punkt):
        return self.__plansza[punkt.get_y()-1][punkt.get_x()-1]

    def wykonaj_ture(self):
        self.__lista_komunikatow.clear()
        do_usuniecia = []
        for organizm in self.__lista_organizmow:
            if organizm.czy_zyje():
                organizm.akcja()
                organizm.postarzej()
                if isinstance(organizm, Zwierze):
                    organizm.ustaw_plodnosc(True)
            else:
                do_usuniecia.append(organizm)
        for organizm in do_usuniecia:
            if self.__plansza[organizm.polozenie.get_y()-1][organizm.polozenie.get_x()-1] is organizm:
                self.__plansza[organizm.polozenie.get_y() - 1][organizm.polozenie.get_x() - 1] = None
            self.__lista_organizmow.remove(organizm)

    def aktualizuj_mape(self, stare, nowe):
        organizm = self.znajdz_organizm(stare)
        self.__plansza[stare.get_y()-1][stare.get_x()-1] = None
        self.__plansza[nowe.get_y() - 1][nowe.get_x() - 1] = organizm

    def dodaj_organizm(self, organizm):
        if organizm is not None:
            self.__plansza[organizm.polozenie.get_y()-1][organizm.polozenie.get_x()-1] = organizm
            self.__lista_organizmow.append(organizm)
            if isinstance(organizm, Zwierze):
                self.__lista_organizmow.sort(key=lambda x: (x.get_inicjatywa(), x.get_wiek()), reverse=True)

    def wprowadz_organizm(self, x, y, gatunek, obraz):
        for pole in self.__lista_pol:
            x1, y1, x2, y2 = obraz.coords(pole)
            poly = geometry.Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
            if poly.contains(geometry.Point(x, y)):
                tab_x = self.__lista_pol.index(pole)
                tab_y = int(tab_x // self.szerokosc)
                tab_x = int(tab_x % self.szerokosc)
                polozenie = Wspolrzedne(tab_x+1, tab_y+1)
                if self.znajdz_organizm(polozenie) is None or not self.znajdz_organizm(polozenie).czy_zyje():
                    organizm_do_dodania = self.stworz_organizm(gatunek, polozenie)
                    if organizm_do_dodania is not None:
                        self.dodaj_organizm(organizm_do_dodania)
                        self.dodaj_komunikat("Dodano nowy organizm\n" + str(polozenie))
                    else:
                        self.dodaj_komunikat("Czlowiek juz istnieje!")
                elif self.znajdz_organizm(polozenie) is not None:
                    self.znajdz_organizm(polozenie).umrzyj()
                    if self.znajdz_organizm(polozenie) is not None and not self.znajdz_organizm(polozenie).czy_zyje():
                        self.dodaj_komunikat("Usunieto organizm\n" + str(polozenie))

    def stworz_organizm(self, gatunek, polozenie):
        organizmy = {
            'CyberOwca': None,
            'Owca': Owca,
            'Wilk': Wilk,
            'Zolw': Zolw,
            'Lis': Lis,
            'Antylopa': Antylopa,
            'Trawa': Trawa,
            'Mlecz': Mlecz,
            'Guarana': Guarana,
            'WilczeJagody': WilczeJagody,
            'BarszczSosnowskiego':BarszczSosnowskiego,
            'Czlowiek': Czlowiek,
        }
        organizm = organizmy[gatunek]
        if organizm is Czlowiek and not any(x.nazwa() == 'czlowiek' and x.czy_zyje()  for x in self.__lista_organizmow):
            return organizm(polozenie, self)
        if organizm is not Czlowiek:
            return organizm(polozenie, self)
        return None

    def dodaj_komunikat(self, wiadomosc):
        self.__lista_komunikatow.append(wiadomosc)

    def wypisz_komunikaty(self, komunikaty):
        if isinstance(komunikaty, StringVar):
            i = 1
            text = "Komunikaty:\n"
            for komunikat in self.__lista_komunikatow:
                text += str(i) + ". " + komunikat + "\n"
                i += 1
            komunikaty.set(text)

    def wydaj_polecenie(self):
        tmp = self.polecenie
        self.polecenie = None
        return tmp

    def zapisz_polecenie(self, polecenie):
        self.polecenie = polecenie

    def stworz_losowy(self, polozenie):
        organizmy = {
            1: Owca,
            2: Wilk,
            3: Zolw,
            4: Lis,
            5: Antylopa,
            6: Trawa,
            7: Mlecz,
            8: Guarana,
            9: WilczeJagody,
            10: BarszczSosnowskiego,
        }
        do_stworzenia = organizmy[randint(1, 10)]
        return do_stworzenia(polozenie, self)



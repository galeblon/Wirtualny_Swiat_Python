from Wspolrzedne import *
from random import *
from Zwierze import *
from shapely import geometry
from SwiatBaza import SwiatBaza
from math import *


class SwiatHex(SwiatBaza):
    def __init__(self, wysokosc, szerokosc):
        super().__init__(wysokosc, szerokosc)

    def rysuj_swiat(self, obraz):
        wymiar_hex = min(obraz.winfo_height()*2/((self.wysokosc+1)*sqrt(3)),
                            obraz.winfo_width()/(self.szerokosc*3))
        wysokosc_hex = wymiar_hex*sqrt(3)/2
        self._lista_pol.clear()
        for y in range(self.wysokosc):
            offset = wymiar_hex-(y % 2)*1.5*wymiar_hex + 2*wymiar_hex
            for x in range(self.szerokosc):
                points = [
                    int(x*2*wymiar_hex+offset), int(y*wysokosc_hex),
                    int(x*2*wymiar_hex+wymiar_hex+offset), int(y*wysokosc_hex),
                    int(x*2*wymiar_hex+1.5*wymiar_hex+offset), int(wysokosc_hex+y*wysokosc_hex),
                    int(x*2*wymiar_hex+wymiar_hex+offset), int(2*wysokosc_hex+y*wysokosc_hex),
                    int(x*2*wymiar_hex+offset), int(2*wysokosc_hex+y*wysokosc_hex),
                    int(x*2*wymiar_hex-0.5*wymiar_hex+offset), int(y*wysokosc_hex+ wysokosc_hex)
                ]
                kolor = 'plum4'
                nazwa = ''
                if self._plansza[y][x] is not None and self._plansza[y][x].czy_zyje():
                    kolor, nazwa = self._plansza[y][x].rysowanie(obraz)
                    nazwa = str(self._lista_organizmow.index(self._plansza[y][x])) + nazwa
                self._lista_pol.append(obraz.create_polygon(points, fill=kolor, outline='black'))
                if int(wymiar_hex // 6) > 1:
                    obraz.create_text(int(x*2*wymiar_hex+offset+0.3*wymiar_hex),
                                      int((y+1)*wysokosc_hex),
                                      fill='black',
                                      font=('Helvetica', int(wymiar_hex // 6)),
                                      text=nazwa, width=wymiar_hex)
                if self._plansza[y][x] is not None \
                        and int(wymiar_hex // 7) > 1 \
                        and isinstance(self._plansza[y][x], Zwierze) is True \
                        and not self._plansza[y][x].czy_dorosly() \
                        and self._plansza[y][x].czy_zyje():
                    obraz.create_text(int(x*2*wymiar_hex+offset + 0.5*wymiar_hex),
                                      int((y + 1.2) * wysokosc_hex),
                                      fill='black',
                                      font=('Helvetica', int(wymiar_hex // 6)), text='dziecko', width=wymiar_hex)
                offset = (x+3)*wymiar_hex + wymiar_hex - (y % 2)*1.5*wymiar_hex

    def znajdz_wolne_sasiadujace(self, pozycja):
        nowe = Wspolrzedne(pozycja.get_x(), pozycja.get_y())
        poprawne_pola = []
        for y in range(-2, 3):
            if y != 0:
                nowe.set_xy(pozycja.get_x(), pozycja.get_y() + y)
                if self.czy_punkt_nalezy(nowe) \
                        and (self.znajdz_organizm(nowe) is None
                             or not self.znajdz_organizm(nowe).czy_zyje()):
                    poprawne_pola.append(Wspolrzedne(nowe.get_x(), nowe.get_y()))
        if pozycja.get_y() % 2 == 0:
            x = -1
        else:
            x = 1
        for y in range(-1, 2):
            if y != 0:
                nowe.set_xy(pozycja.get_x() + x, pozycja.get_y() + y)
                if self.czy_punkt_nalezy(nowe) \
                        and (self.znajdz_organizm(nowe) is None
                             or not self.znajdz_organizm(nowe).czy_zyje()):
                    poprawne_pola.append(Wspolrzedne(nowe.get_x(), nowe.get_y()))
        if len(poprawne_pola) != 0:
            return poprawne_pola[randint(0, len(poprawne_pola) - 1)]
        return None

    def znajdz_sasiadujace(self, pozycja):
        nowe = Wspolrzedne(pozycja.get_x(), pozycja.get_y())
        poprawne_pola = []
        for y in range(-2, 3):
            if y != 0:
                nowe.set_xy(pozycja.get_x(), pozycja.get_y()+y)
                if self.czy_punkt_nalezy(nowe):
                    poprawne_pola.append(Wspolrzedne(nowe.get_x(), nowe.get_y()))
        if pozycja.get_y() % 2 == 0:
            x = -1
        else:
            x = 1
        for y in range(-1, 2):
            if y != 0:
                nowe.set_xy(pozycja.get_x()+x, pozycja.get_y()+y)
                if self.czy_punkt_nalezy(nowe):
                    poprawne_pola.append(Wspolrzedne(nowe.get_x(), nowe.get_y()))
        if len(poprawne_pola) != 0:
            return poprawne_pola[randint(0, len(poprawne_pola)-1)]
        return None

    def znajdz_sasiadujace_pola(self, pozycja):
        nowe = Wspolrzedne(pozycja.get_x(), pozycja.get_y())
        poprawne_pola = []
        for y in range(-2, 3):
            if y != 0:
                nowe.set_xy(pozycja.get_x(), pozycja.get_y() + y)
                if self.czy_punkt_nalezy(nowe):
                    poprawne_pola.append(Wspolrzedne(nowe.get_x(), nowe.get_y()))
        if pozycja.get_y() % 2 == 0:
            x = -1
        else:
            x = 1
        for y in range(-1, 2):
            if y != 0:
                nowe.set_xy(pozycja.get_x() + x, pozycja.get_y() + y)
                if self.czy_punkt_nalezy(nowe):
                    poprawne_pola.append(Wspolrzedne(nowe.get_x(), nowe.get_y()))
        if len(poprawne_pola) != 0:
            return poprawne_pola
        return None

    def znajdz_sasiadujace_klawisz(self, pozycja, kierunek):
        ruchy = {
            "Up": (0, -2),
            "Down": (0, 2),
            "w": (0, -2),
            "x": (0, 2),
            "e": (pozycja.get_y() % 2, -1),
            "q": (-(pozycja.get_y() % 2 == 0), -1),
            "z": (-(pozycja.get_y() % 2 == 0), 1),
            "c": (pozycja.get_y() % 2, 1),
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

    def wprowadz_organizm(self, x, y, gatunek, obraz):
        for pole in self._lista_pol:
            x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6 = obraz.coords(pole)
            poly = geometry.Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6)])
            if poly.contains(geometry.Point(x, y)):
                tab_x = self._lista_pol.index(pole)
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
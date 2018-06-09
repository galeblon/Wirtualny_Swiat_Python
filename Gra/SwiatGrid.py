from Wspolrzedne import *
from random import *
from Zwierze import *
from shapely import geometry
from SwiatBaza import SwiatBaza


class SwiatGrid(SwiatBaza):
    def __init__(self, wysokosc, szerokosc):
        super().__init__(wysokosc, szerokosc)

    def rysuj_swiat(self, obraz):
        rozmiar_kraty = min(obraz.winfo_height()/self.wysokosc, obraz.winfo_width()/self.szerokosc)
        self._lista_pol.clear()
        for y in range(self.wysokosc):
            for x in range(self.szerokosc):
                kolor = 'saddle brown'
                nazwa = ''
                if self._plansza[y][x] is not None and self._plansza[y][x].czy_zyje():
                    kolor, nazwa = self._plansza[y][x].rysowanie(obraz)
                    nazwa = str(self._lista_organizmow.index(self._plansza[y][x])) + nazwa
                self._lista_pol.append(obraz.create_rectangle(x*rozmiar_kraty, y*rozmiar_kraty, (x+1)*rozmiar_kraty,
                                        (y+1)*rozmiar_kraty, fill=kolor))
                if int(rozmiar_kraty // 6) > 1:
                    obraz.create_text((x + 0.5) * rozmiar_kraty, (y + 0.4) * rozmiar_kraty, fill='black',
                                      font=('Helvetica', int(rozmiar_kraty // 7)),
                                      text=nazwa, width=rozmiar_kraty)
                if self._plansza[y][x] is not None \
                        and int(rozmiar_kraty // 7) > 1 \
                        and isinstance(self._plansza[y][x], Zwierze) is True \
                        and not self._plansza[y][x].czy_dorosly() \
                        and self._plansza[y][x].czy_zyje():
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

    def wprowadz_organizm(self, x, y, gatunek, obraz):
        for pole in self._lista_pol:
            x1, y1, x2, y2 = obraz.coords(pole)
            poly = geometry.Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
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
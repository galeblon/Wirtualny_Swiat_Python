import random

from Zwierze import *
from random import *


class Zolw(Zwierze):
    def __init__(self, start, swiat):
        super(Zwierze, self).__init__(2, 1, start, swiat)

    def rysowanie(self, okno):
        return 'dark olive green', 'zolw'

    def utworz_dziecko(self, polozenie):
        self.swiat.dodaj_komunikat("Narodzil sie nowy zolw!\n" + str(self.polozenie))
        return Zolw(polozenie, self.swiat)

    def nazwa(self):
        return 'zolw'

    def akcja(self):
        if self.get_wiek() < 1:
            return
        if randint(0, 100) <= 75:
            return
        super().akcja()

    def kolizja(self, atakujacy):
        if isinstance(atakujacy, Zwierze):
            if type(atakujacy) is type(self):
                if self.czy_dorosly() and self.czy_plodny() and atakujacy.czy_plodny() and atakujacy.czy_dorosly():
                    wolne = self.swiat.znajdz_wolne_sasiadujace(self.polozenie)
                    if wolne is not None:
                        self.swiat.dodaj_organizm(self.utworz_dziecko(wolne))
                        self.ustaw_plodnosc(False)
                        atakujacy.ustaw_plodnosc(False)
            else:
                if atakujacy.get_sila() < 5:
                    self.swiat.dodaj_komunikat(atakujacy.nazwa() + " nie jest w stanie\nprzebic pancerza zolwia.")
                    return
                if self.get_sila() > atakujacy.get_sila():
                    atakujacy.umrzyj()
                    if not atakujacy.czy_zyje():
                        self.swiat.dodaj_komunikat(self.nazwa() + ' zabija ' + atakujacy.nazwa())
                else:
                    self.umrzyj()
                    if not self.czy_zyje():
                        self.swiat.dodaj_komunikat(atakujacy.nazwa() + ' zabija ' + self.nazwa())

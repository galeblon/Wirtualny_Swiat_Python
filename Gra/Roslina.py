from random import *
from Zwierze import *


class Roslina(Organizm):

    def __init__(self, sila, start, swiat):
        self.plodny = 1
        super().__init__(sila, 0, start, swiat)

    def akcja(self):
        if randint(1, 100) <= 1:
            nowe = self.swiat.znajdz_wolne_sasiadujace(self.polozenie)
            if nowe is not None:
                self.swiat.dodaj_organizm(self.utworz_dziecko(nowe))

    def kolizja(self, atakujacy):
        if isinstance(atakujacy, Zwierze):
            self.umrzyj()
            if not self.czy_zyje():
                self.swiat.dodaj_komunikat(atakujacy.nazwa() + ' zjada ' + self.nazwa())
            if self.get_sila() > atakujacy.get_sila():
                atakujacy.umrzyj()
                if not atakujacy.czy_zyje():
                    self.swiat.dodaj_komunikat(self.nazwa() + ' zatruwa ' + atakujacy.nazwa())

    def nazwa(self):
        return 'Roslina'

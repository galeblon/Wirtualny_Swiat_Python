from Zwierze import *
from random import *


class Antylopa(Zwierze):
    def __init__(self, start, swiat):
        super(Zwierze, self).__init__(4, 4, start, swiat)

    def rysowanie(self, okno):
        return 'sandy brown', 'antylopa'

    def utworz_dziecko(self, polozenie):
        self.swiat.dodaj_komunikat("Narodzila sie nowa antylopa!\n" + str(self.polozenie))
        return Antylopa(polozenie, self.swiat)

    def nazwa(self):
        return 'antylopa'

    def akcja(self):
        if self.get_wiek() < 1:
            return
        for i in range(0, randint(1, 2)):
            if self.czy_zyje() is True:
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
                if randint(0,1) == 1:
                    polozenie_temp = self.swiat.znajdz_wolne_sasiadujace(self.polozenie)
                    if polozenie_temp is not None:
                        self.swiat.dodaj_komunikat("Antylopa ucieka przed " + atakujacy.nazwa()
                                                   + "\n" + str(self.polozenie))
                        self.swiat.aktualizuj_mape(self.polozenie, polozenie_temp)
                        self.polozenie = polozenie_temp
                        return
                    else:
                        self.swiat.dodaj_komunikat("Antylopa nie ma dokad uciekac\n" + str(self.polozenie))
                if self.get_sila() > atakujacy.get_sila():
                    atakujacy.umrzyj()
                    if not atakujacy.czy_zyje():
                        self.swiat.dodaj_komunikat(self.nazwa() + ' zabija ' + atakujacy.nazwa())
                else:
                    self.umrzyj()
                    if not self.czy_zyje():
                        self.swiat.dodaj_komunikat(atakujacy.nazwa() + ' zabija ' + self.nazwa())


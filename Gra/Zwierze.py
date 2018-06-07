from Organizm import *


class Zwierze(Organizm):

    plodny = 1

    def __init__(self, sila, inicjatywa, start, swiat):
        self.plodny = 1
        super(Organizm, self).__init__(sila, inicjatywa, start, swiat)

    def akcja(self):
        if self.get_wiek() < 1:
            return
        polozenie_temp = self.swiat.znajdz_sasiadujace(self.polozenie)
        if polozenie_temp is not None:
            if self.swiat.znajdz_organizm(polozenie_temp) is not None and self.swiat.znajdz_organizm(polozenie_temp).czy_zyje():
                self.swiat.znajdz_organizm(polozenie_temp).kolizja(self)
            if self.czy_zyje() and (self.swiat.znajdz_organizm(polozenie_temp) is None or not self.swiat.znajdz_organizm(polozenie_temp).czy_zyje()):
                self.swiat.aktualizuj_mape(self.polozenie, polozenie_temp)
                self.polozenie = polozenie_temp

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
                if self.get_sila() > atakujacy.get_sila():
                    atakujacy.umrzyj()
                else:
                    self.umrzyj()
        pass

    def czy_dorosly(self):
        return self.get_wiek() > 5

    def czy_plodny(self):
        return self.plodny > 0

    def ustaw_plodnosc(self, wskaz):
        if wskaz is True and self.plodny <= 0:
            self.plodny = self.plodny + 1
        elif wskaz is False:
            self.plodny = -5


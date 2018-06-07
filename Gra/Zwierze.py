from Organizm import *


class Zwierze(Organizm):

    plodny = 1

    def __init__(self, sila, inicjatywa, start, swiat):
        self.plodny = 1
        super(Organizm, self).__init__(sila, inicjatywa, start, swiat)

    def akcja(self):
        if self.get_wiek() < 1:
            return
        polozenie_temp = self.swiat.znajdz_wolne_sasiadujace(self.polozenie)
        if polozenie_temp is not None:
            self.swiat.aktualizuj_mape(self.polozenie, polozenie_temp)
            self.polozenie = polozenie_temp

    def kolizja(self, atakujacy):
        pass

    def czy_dorosly(self):
        return self.get_wiek() < 5

    def czy_plodny(self):
        return self.plodny > 0

    def ustaw_plodnosc(self, wskaz):
        if wskaz and self.plodny <= 0:
            self.plodny = self.plodny + 1
        else:
            self.plodny = -5


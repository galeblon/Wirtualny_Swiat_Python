from Zwierze import *


class Lis(Zwierze):
    def __init__(self, start, swiat):
        super(Zwierze, self).__init__(3, 7, start, swiat)

    def rysowanie(self, okno):
        return 'firebrick', 'lis'

    def utworz_dziecko(self, polozenie):
        self.swiat.dodaj_komunikat("Narodzil sie nowy lis!\n" + str(self.polozenie))
        return Lis(polozenie, self.swiat)

    def nazwa(self):
        return 'lis'

    def akcja(self):
        if self.get_wiek() < 1:
            return
        polozenie_temp = self.swiat.znajdz_sasiadujace(self.polozenie)
        if polozenie_temp is not None:
            if self.swiat.znajdz_organizm(polozenie_temp) is not None \
                    and self.swiat.znajdz_organizm(polozenie_temp).czy_zyje():
                if self.swiat.znajdz_organizm(polozenie_temp).get_sila() <= self.get_sila():
                    self.swiat.znajdz_organizm(polozenie_temp).kolizja(self)
                else:
                    self.swiat.dodaj_komunikat("Lis unika kontaktu\nz silniejszym organizmem.")
                    polozenie_temp = self.swiat.znajdz_wolne_sasiadujace(polozenie_temp)
                    if polozenie_temp is not None:
                        self.swiat.aktualizuj_mape(self.polozenie, polozenie_temp)
                        self.polozenie = polozenie_temp
            if self.czy_zyje() and (self.swiat.znajdz_organizm(polozenie_temp) is None or not self.swiat.znajdz_organizm(polozenie_temp).czy_zyje()):
                self.swiat.aktualizuj_mape(self.polozenie, polozenie_temp)
                self.polozenie = polozenie_temp


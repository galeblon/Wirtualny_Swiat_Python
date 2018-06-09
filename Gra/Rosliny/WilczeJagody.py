from Roslina import *


class WilczeJagody(Roslina):
    def __init__(self, start, swiat):
        super().__init__(99, start, swiat)

    def rysowanie(self, okno):
        return 'RoyalBlue2', 'wilcze jagody'

    def utworz_dziecko(self, polozenie):
        self.swiat.dodaj_komunikat("Wyroslo nowe pole wilczych jagod.\n" + str(self.polozenie))
        return WilczeJagody(polozenie, self.swiat)

    def nazwa(self):
        return 'wilcze jagody'

    def kolizja(self, atakujacy):
        if isinstance(atakujacy, Zwierze):
            self.umrzyj()
            if not self.czy_zyje():
                self.swiat.dodaj_komunikat(atakujacy.nazwa() + ' zjada ' + self.nazwa())
            atakujacy.umrzyj()
            if not atakujacy.czy_zyje():
                self.swiat.dodaj_komunikat(self.nazwa() + ' zatruwa ' + atakujacy.nazwa())

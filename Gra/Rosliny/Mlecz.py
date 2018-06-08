from Roslina import *


class Mlecz(Roslina):
    def __init__(self, start, swiat):
        super().__init__(0, start, swiat)

    def rysowanie(self, okno):
        return 'goldenrod1', 'mlecz'

    def utworz_dziecko(self, polozenie):
        self.swiat.dodaj_komunikat("Wyroslo nowe pole mleczu.\n" + str(self.polozenie))
        return Mlecz(polozenie, self.swiat)

    def nazwa(self):
        return 'mlecz'

    def akcja(self):
        for i in range(0, 3):
            super().akcja()

from Roslina import *


class Trawa(Roslina):
    def __init__(self, start, swiat):
        super().__init__(0, start, swiat)

    def rysowanie(self, okno):
        return 'forest green', 'trawa'

    def utworz_dziecko(self, polozenie):
        self.swiat.dodaj_komunikat("Wyroslo nowe pole trawy.\n" + str(self.polozenie))
        return Trawa(polozenie, self.swiat)

    def nazwa(self):
        return 'trawa'

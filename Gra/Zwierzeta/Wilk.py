from Zwierze import *


class Wilk(Zwierze):
    def __init__(self, start, swiat):
        super(Zwierze, self).__init__(9, 4, start, swiat)

    def rysowanie(self, okno):
        return 'grey', 'willk'

    def utworz_dziecko(self, polozenie):
        return Wilk(polozenie, self.swiat)

    def nazwa(self):
        return 'wilk'
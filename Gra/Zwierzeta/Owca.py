from Zwierze import *


class Owca(Zwierze):
    def __init__(self, start, swiat):
        super(Zwierze, self).__init__(4, 4, start, swiat)

    def rysowanie(self, okno):
        return 'white', 'owca'

    def utworz_dziecko(self, polozenie):
        pass

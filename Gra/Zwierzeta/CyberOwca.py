from Zwierzeta.Owca import Owca


class CyberOwca(Owca):
    def __init__(self, start, swiat):
        super().__init__(start, swiat)
        self.set_sila(11)

    def rysowanie(self, okno):
        return 'plum1', 'cyber-owca'

    def utworz_dziecko(self, polozenie):
        self.swiat.dodaj_komunikat("Narodzila sie nowa owca!\n" + str(self.polozenie))
        return Owca(polozenie, self.swiat)

    def nazwa(self):
        return 'cyber-owca'

    def akcja(self):
        super().akcja()

    def kolizja(self, atakujacy):
        super().kolizja(atakujacy)
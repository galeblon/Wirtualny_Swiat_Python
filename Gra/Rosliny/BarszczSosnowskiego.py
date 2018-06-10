from Roslina import *


class BarszczSosnowskiego(Roslina):
    def __init__(self, start, swiat):
        super().__init__(10, start, swiat)

    def rysowanie(self, okno):
        return 'dark sea green', 'barszcz sosnowskiego'

    def utworz_dziecko(self, polozenie):
        self.swiat.dodaj_komunikat("Wyroslo nowe pole barszczu sosnowskiego.\n" + str(self.polozenie))
        return BarszczSosnowskiego(polozenie, self.swiat)

    def nazwa(self):
        return 'barszcz sosnowskiego'

    def akcja(self):
        sasiadujace = self.swiat.znajdz_sasiadujace_pola(self.polozenie)
        for sasiad_punkt in sasiadujace:
            sasiad = self.swiat.znajdz_organizm(sasiad_punkt)
            if sasiad is not None and isinstance(sasiad, Zwierze) and sasiad.czy_zyje():
                sasiad.umrzyj(self)
                if not sasiad.czy_zyje():
                    self.swiat.dodaj_komunikat("Barszcz parzy " + sasiad.nazwa() + "\n" + str(sasiad_punkt))
        super().akcja()

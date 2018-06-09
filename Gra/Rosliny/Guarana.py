from Roslina import *


class Guarana(Roslina):
    def __init__(self, start, swiat):
        super().__init__(0, start, swiat)

    def rysowanie(self, okno):
        return 'firebrick1', 'guarana'

    def utworz_dziecko(self, polozenie):
        self.swiat.dodaj_komunikat("Wyroslo nowe pole guarany.\n" + str(self.polozenie))
        return Guarana(polozenie, self.swiat)

    def nazwa(self):
        return 'guarana'

    def kolizja(self, atakujacy):
        if isinstance(atakujacy, Zwierze):
            self.umrzyj()
            if not self.czy_zyje():
                self.swiat.dodaj_komunikat(atakujacy.nazwa() + ' zjada ' + self.nazwa())
                atakujacy.zwieksz_sile(3)
                self.swiat.dodaj_komunikat(atakujacy.nazwa() + ' zwieksza swoja sile o 3\n(teraz ' + str(atakujacy.get_sila()) + ')')
            if self.get_sila() > atakujacy.get_sila():
                atakujacy.umrzyj()
                if not atakujacy.czy_zyje():
                    self.swiat.dodaj_komunikat(self.nazwa() + ' zatruwa ' + atakujacy.nazwa())

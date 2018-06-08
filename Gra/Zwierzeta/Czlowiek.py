from Zwierze import *


class Czlowiek(Zwierze):
    def __init__(self, start, swiat):
        self.licznik_umiejetnosci = 0
        self.umiejetnosc_aktywna = False
        super(Zwierze, self).__init__(5, 4, start, swiat)

    def rysowanie(self, okno):
        return '#E8C7BB', 'czlowiek'

    def utworz_dziecko(self, polozenie):
        return Czlowiek(polozenie, self.swiat)

    def nazwa(self):
        return 'czlowiek'

    def akcja(self):
        polecenie = self.swiat.wydaj_polecenie()
        polozenie_temp = None
        if polecenie is not None:
            polozenie_temp = self.swiat.znajdz_sasiadujace_klawisz(self.polozenie, polecenie)
            if polecenie == 'space':
                self.aktywuj_umiejetnosc()
        if polozenie_temp is not None:
            if self.swiat.znajdz_organizm(polozenie_temp) is not None and self.swiat.znajdz_organizm(polozenie_temp).czy_zyje():
                self.swiat.znajdz_organizm(polozenie_temp).kolizja(self)
            if self.czy_zyje() and (self.swiat.znajdz_organizm(polozenie_temp) is None or not self.swiat.znajdz_organizm(polozenie_temp).czy_zyje()):
                self.swiat.aktualizuj_mape(self.polozenie, polozenie_temp)
                self.polozenie = polozenie_temp
        if self.umiejetnosc_aktywna is True:
            self.licznik_umiejetnosci -= 1
            if self.licznik_umiejetnosci <= 0:
                self.umiejetnosc_aktywna = False
                self.swiat.dodaj_komunikat("Umiejetnosc sie wyczerpala.")
            else:
                self.swiat.dodaj_komunikat("Pozostalo " + str(self.licznik_umiejetnosci) + "tur \nniesmiertelnosci.")
        elif self.licznik_umiejetnosci <= 5:
            self.licznik_umiejetnosci += 1

    def aktywuj_umiejetnosc(self):
        if self.umiejetnosc_aktywna is True:
            self.swiat.dodaj_komunikat("Umiejetnosc jest juz aktywna.")
        elif self.licznik_umiejetnosci < 5:
            self.swiat.dodaj_komunikat("Pozostalo " + str(5-self.licznik_umiejetnosci) +
                                       " tur zanim\numiejetnosc bedzie gotowa")
        else:
            self.umiejetnosc_aktywna = True
            self.swiat.dodaj_komunikat("Aktywowano niesmiertelnosc\nna 5 tur.")

    def umrzyj(self):
        if not self.umiejetnosc_aktywna:
            super(Zwierze, self).umrzyj()
        else:
            self.unik()
            self.swiat.dodaj_komunikat("Czlowiek unika smierci!")

    def unik(self):
        nowe = self.swiat.znajdz_wolne_sasiadujace(self.polozenie)
        if nowe is not None:
            self.swiat.aktualizuj_mape(self.polozenie, nowe)
            self.polozenie = nowe

    def dane_do_zapisu(self):
        zapis = super().dane_do_zapisu()
        zapis += ";" + str(self.umiejetnosc_aktywna) + ";" + str(self.licznik_umiejetnosci)
        return zapis

    def set_aktywna_umiejetnosc(self, val):
        self.umiejetnosc_aktywna = val

    def set_licznik(self, val):
        self.licznik_umiejetnosci = val
from Zwierzeta.Owca import Owca
from Rosliny.BarszczSosnowskiego import BarszczSosnowskiego


class CyberOwca(Owca):
    def __init__(self, start, swiat):
        super().__init__(start, swiat)
        self.set_sila(11)
        self.cel = None
        self.sciezka = []

    def rysowanie(self, okno):
        return 'plum1', 'cyber-owca'

    def utworz_dziecko(self, polozenie):
        return None

    def nazwa(self):
        return 'cyber-owca'

    def akcja(self):
        self.szukaj_barszczu()
        if len(self.sciezka) > 0:
            polozenie_temp = self.sciezka.pop(1)
            if polozenie_temp is not None:
                if self.swiat.znajdz_organizm(polozenie_temp) is not None \
                   and self.swiat.znajdz_organizm(polozenie_temp).czy_zyje() \
                   and self.swiat.znajdz_organizm(polozenie_temp).get_sila() > self.get_sila():
                    self.szukaj_barszczu(True)
                    return
                if self.swiat.znajdz_organizm(polozenie_temp) is not None and self.swiat.znajdz_organizm(
                        polozenie_temp).czy_zyje():
                    self.swiat.znajdz_organizm(polozenie_temp).kolizja(self)
                if self.czy_zyje() and (
                        self.swiat.znajdz_organizm(polozenie_temp) is None or not self.swiat.znajdz_organizm(
                        polozenie_temp).czy_zyje()):
                    self.swiat.aktualizuj_mape(self.polozenie, polozenie_temp)
                    self.polozenie = polozenie_temp
                else:
                    self.sciezka.clear()
                    self.cel = None
        else:
            super().akcja()

    def kolizja(self, atakujacy):
        super().kolizja(atakujacy)

    def umrzyj(self, powod=None):
        if isinstance(powod, BarszczSosnowskiego):
            return
        super().umrzyj(powod)

    def szukaj_barszczu(self, reset=False):
        if self.cel is not None and isinstance(self.swiat.znajdz_organizm(self.cel), BarszczSosnowskiego) \
           and self.swiat.znajdz_organizm(self.cel).czy_zyje() and reset is False:
            return
        self.sciezka.clear()
        self.cel = None
        plansza = [[{'kolor': 'w', 'dystans': 'inf', 'prev': None} for x in range(self.swiat.szerokosc)]
                   for y in range(self.swiat.wysokosc)]
        pola = [self.polozenie]
        plansza[self.polozenie.get_y()-1][self.polozenie.get_x()-1]['kolor'] = 'g'
        plansza[self.polozenie.get_y()-1][self.polozenie.get_x()-1]['dystans'] = 0
        while len(pola) != 0:
            pole = pola.pop(0)
            for sasiad in self.swiat.znajdz_sasiadujace_pola(pole):
                if self.swiat.znajdz_organizm(sasiad) is None \
                        or not self.swiat.znajdz_organizm(sasiad).czy_zyje() \
                        or self.swiat.znajdz_organizm(sasiad).get_sila() <= self.get_sila():
                    if plansza[sasiad.get_y()-1][sasiad.get_x()-1]['dystans'] == 'inf'\
                       or plansza[sasiad.get_y() - 1][sasiad.get_x() - 1]['dystans'] > \
                            plansza[pole.get_y() - 1][pole.get_x() - 1]['dystans'] + 1:
                        plansza[sasiad.get_y() - 1][sasiad.get_x() - 1]['dystans'] = \
                            plansza[pole.get_y() - 1][pole.get_x() - 1]['dystans'] + 1
                        plansza[sasiad.get_y() - 1][sasiad.get_x() - 1]['prev'] = pole
                    if plansza[sasiad.get_y()-1][sasiad.get_x()-1]['kolor'] == 'w':
                        plansza[sasiad.get_y()-1][sasiad.get_x()-1]['kolor'] = 'g'
                        if self.cel is None or plansza[sasiad.get_y() - 1][sasiad.get_x() - 1]['dystans'] < \
                                plansza[self.cel.get_y() - 1][self.cel.get_x() - 1]['dystans']:
                            pola.append(sasiad)
                        else:
                            plansza[sasiad.get_y() - 1][sasiad.get_x() - 1]['kolor'] = 'b'
                    if isinstance(self.swiat.znajdz_organizm(sasiad), BarszczSosnowskiego) \
                            and (self.cel is None or plansza[sasiad.get_y() - 1][sasiad.get_x() - 1]['dystans'] <
                                 plansza[self.cel.get_y() - 1][self.cel.get_x() - 1]['dystans']):
                        self.cel = sasiad
            plansza[pole.get_y()-1][pole.get_x()-1]['kolor'] = 'b'
        tmp = self.cel
        if tmp is None:
            return
        while plansza[tmp.get_y()-1][tmp.get_x()-1]['prev'] is not None:
            self.sciezka.append(tmp)
            tmp = plansza[tmp.get_y()-1][tmp.get_x()-1]['prev']
        self.sciezka.append(tmp)
        self.sciezka.reverse()

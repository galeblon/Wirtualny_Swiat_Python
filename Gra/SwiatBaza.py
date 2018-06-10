from Wspolrzedne import *
from random import *
from Zwierze import *
from Zwierzeta.Wilk import Wilk
from Zwierzeta.Owca import Owca
from Zwierzeta.Zolw import Zolw
from Zwierzeta.Lis import Lis
from Zwierzeta.Antylopa import Antylopa
from Zwierzeta.CyberOwca import CyberOwca
from Rosliny.Trawa import Trawa
from Rosliny.Mlecz import Mlecz
from Rosliny.Guarana import Guarana
from Rosliny.WilczeJagody import WilczeJagody
from Rosliny.BarszczSosnowskiego import BarszczSosnowskiego
from Zwierzeta.Czlowiek import Czlowiek
from tkinter import StringVar
from abc import ABC, abstractmethod


class SwiatBaza(ABC):
    def __init__(self, wysokosc, szerokosc):
        self.wysokosc = wysokosc
        self.szerokosc = szerokosc
        self.polecenie = None
        self._lista_organizmow = []
        self._lista_komunikatow = []
        self._lista_pol = []
        self._plansza = [[None for x in range(szerokosc)] for y in range(wysokosc)]

    @abstractmethod
    def rysuj_swiat(self, obraz):
        pass

    @abstractmethod
    def znajdz_wolne_sasiadujace(self, pozycja):
        pass

    @abstractmethod
    def znajdz_sasiadujace(self, pozycja):
        pass

    @abstractmethod
    def znajdz_sasiadujace_pola(self, pozycja):
        pass

    @abstractmethod
    def znajdz_sasiadujace_klawisz(self, pozycja, kierunek):
        pass

    @abstractmethod
    def wprowadz_organizm(self, x, y, gatunek, obraz):
        pass

    def czy_punkt_nalezy(self, punkt):
        if 0 < punkt.get_x() <= self.szerokosc:
            if 0 < punkt.get_y() <= self.wysokosc:
                return True
        return False

    def znajdz_organizm(self, punkt):
        return self._plansza[punkt.get_y()-1][punkt.get_x()-1]

    def wykonaj_ture(self):
        self._lista_komunikatow.clear()
        do_usuniecia = []
        for organizm in self._lista_organizmow:
            if organizm.czy_zyje():
                organizm.akcja()
                organizm.postarzej()
                if isinstance(organizm, Zwierze):
                    organizm.ustaw_plodnosc(True)
            else:
                do_usuniecia.append(organizm)
        for organizm in do_usuniecia:
            if self._plansza[organizm.polozenie.get_y()-1][organizm.polozenie.get_x()-1] is organizm:
                self._plansza[organizm.polozenie.get_y() - 1][organizm.polozenie.get_x() - 1] = None
            self._lista_organizmow.remove(organizm)

    def aktualizuj_mape(self, stare, nowe):
        organizm = self.znajdz_organizm(stare)
        self._plansza[stare.get_y()-1][stare.get_x()-1] = None
        self._plansza[nowe.get_y()-1][nowe.get_x()-1] = organizm

    def dodaj_organizm(self, organizm):
        if organizm is not None:
            self._plansza[organizm.polozenie.get_y()-1][organizm.polozenie.get_x()-1] = organizm
            self._lista_organizmow.append(organizm)
            if isinstance(organizm, Zwierze):
                self._lista_organizmow.sort(key=lambda x: (x.get_inicjatywa(), x.get_wiek()), reverse=True)

    def stworz_organizm(self, gatunek, polozenie):
        organizm = self.mapuj_gatunek(gatunek)
        if organizm is Czlowiek and not any(x.nazwa() == 'czlowiek' and x.czy_zyje() for x in self._lista_organizmow):
            return organizm(polozenie, self)
        if organizm is not Czlowiek:
            return organizm(polozenie, self)
        return None

    def dodaj_komunikat(self, wiadomosc):
        self._lista_komunikatow.append(wiadomosc)

    def wypisz_komunikaty(self, komunikaty):
        if isinstance(komunikaty, StringVar):
            i = 1
            text = "Komunikaty:\n"
            for komunikat in self._lista_komunikatow:
                text += str(i) + ". " + komunikat + "\n"
                i += 1
            komunikaty.set(text)

    def wydaj_polecenie(self):
        tmp = self.polecenie
        self.polecenie = None
        return tmp

    def zapisz_polecenie(self, polecenie):
        self.polecenie = polecenie

    def stworz_losowy(self, polozenie):
        organizmy = {
            1: Owca,
            2: Wilk,
            3: Zolw,
            4: Lis,
            5: Antylopa,
            6: Trawa,
            7: Mlecz,
            8: Guarana,
            9: WilczeJagody,
            10: BarszczSosnowskiego,
            11: CyberOwca,
        }
        do_stworzenia = organizmy[randint(1, 11)]
        return do_stworzenia(polozenie, self)

    def zapisz_organizmy(self, plik):
        for organizm in self._lista_organizmow:
            if organizm.czy_zyje():
                plik.write(organizm.__class__.__name__ + ';')
                plik.write(organizm.dane_do_zapisu() + '\n')

    def wczytaj_organizmy(self, plik):
        for l in plik:
            argumenty = l.split(';')
            try:
                organizm = self.mapuj_gatunek(argumenty[0])
            except KeyError:
                return False
            try:
                lokacja = Wspolrzedne(int(argumenty[3]), int(argumenty[4]))
                if self.znajdz_organizm(lokacja) is not None:
                    return False
                stworzenie = organizm(lokacja, self)
                stworzenie.set_sila(int(argumenty[1]))
                stworzenie.set_wiek(int(argumenty[5]))
                if issubclass(organizm, Zwierze):
                    stworzenie.set_plodnosc(int(argumenty[6]))
                if organizm is Czlowiek:
                    stworzenie.set_aktywna_umiejetnosc(bool(argumenty[7]))
                    stworzenie.set_licznik(int(argumenty[8]))
                self.dodaj_organizm(stworzenie)
            except IndexError:
                return False
            except ValueError:
                return False
        return True

    @staticmethod
    def mapuj_gatunek(gatunek):
        organizmy = {
            'CyberOwca': CyberOwca,
            'Owca': Owca,
            'Wilk': Wilk,
            'Zolw': Zolw,
            'Lis': Lis,
            'Antylopa': Antylopa,
            'Trawa': Trawa,
            'Mlecz': Mlecz,
            'Guarana': Guarana,
            'WilczeJagody': WilczeJagody,
            'BarszczSosnowskiego': BarszczSosnowskiego,
            'Czlowiek': Czlowiek,
        }
        return organizmy[gatunek]

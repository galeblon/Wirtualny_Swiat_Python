from abc import ABC, abstractmethod


class Organizm(ABC):
    def __init__(self, sila, inicjatywa, start, swiat):
        self.__sila = sila
        self.__inicjatywa = inicjatywa
        self.polozenie = start
        self.swiat = swiat
        self.__zyje = True
        self.__wiek = 1

    @abstractmethod
    def akcja(self):
        pass

    @abstractmethod
    def kolizja(self, atakujacy):
        pass

    @abstractmethod
    def rysowanie(self, okno):
        pass

    @abstractmethod
    def utworz_dziecko(self, polozenie):
        pass

    def czy_zyje(self):
        return self.__zyje

    def postarzej(self):
        self.__wiek = self.__wiek + 1

    def umrzyj(self, powod=None):
        self.__zyje = False

    def get_inicjatywa(self):
        return self.__inicjatywa

    def get_wiek(self):
        return self.__wiek

    def get_sila(self):
        return self.__sila

    def dane_do_zapisu(self):
        zapis = ''
        zapis += '{0};{1};{2};{3};{4}'.format(self.__sila, self.__inicjatywa,
                                              self.polozenie.get_x(), self.polozenie.get_y(),
                                              self.__wiek)
        return zapis

    def set_wiek(self, wiek):
        self.__wiek = wiek

    def set_sila(self, val):
        self.__sila = val

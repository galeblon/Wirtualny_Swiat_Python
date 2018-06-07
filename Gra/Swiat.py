from tkinter import Canvas

class Swiat:
    def __init__(self, wysokosc, szerokosc):
        self.wysokosc = wysokosc
        self.szerokosc = szerokosc
        self.__lista_organizmow = []
        self.__lista_komunikatow = []
        self.__lista_pol = []
        self.__plansza = [[None for x in range(szerokosc)] for y in range(wysokosc)]

    def rysuj_swiat(self, obraz):
        #obraz = Canvas()
        rozmiar_kraty = min(obraz.winfo_height()/self.wysokosc, obraz.winfo_width()/self.szerokosc)
        self.__lista_pol.clear()
        for y in range(self.wysokosc):
            for x in range(self.szerokosc):
                obraz.create_rectangle(x*rozmiar_kraty, y*rozmiar_kraty, (x+1)*rozmiar_kraty, (y+1)*rozmiar_kraty, fill='brown')
                obraz.create_text((x+0.5)*rozmiar_kraty, (y+0.4)*rozmiar_kraty, fill='black', font=('Helvetica', int(rozmiar_kraty//6)), text='Test Testowy', width=rozmiar_kraty)


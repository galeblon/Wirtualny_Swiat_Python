from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from Swiat import *
from Zwierzeta.Owca import *
from Zwierzeta.Wilk import *
from Zwierzeta.Czlowiek import *
import sys
sys.setrecursionlimit(10000)


class Okno:
    def __init__(self):
        #self.running = True
        self.okno = Tk()
        self.okno.title("Wirtualny Swiat - Adrian Misiak 171600")
        self.okno.minsize(800, 240)

        self.okno.bind("<Key>", self.key_press)

        self.swiat = Swiat(10, 10)
        self.swiat.dodaj_organizm(Owca(Wspolrzedne(1, 1), self.swiat))
        self.swiat.dodaj_organizm(Owca(Wspolrzedne(3, 3), self.swiat))
        self.swiat.dodaj_organizm(Wilk(Wspolrzedne(8, 8), self.swiat))
        self.swiat.dodaj_organizm(Czlowiek(Wspolrzedne(5, 5), self.swiat))

        self.przyciski = Frame(self.okno, width=330, background='yellow')
        self.n_gra_b = Button(self.przyciski, text="Nowa gra", command=lambda: self.new_game(), width=20)
        self.n_gra_b.pack(side=TOP)
        self.n_tura_b = Button(self.przyciski, text="Nowa tura", command=lambda: self.new_turn())
        self.n_tura_b.pack(side=TOP)
        self.z_gre_b = Button(self.przyciski, text="Zapisz gre")
        self.z_gre_b.pack(side=TOP)
        self.w_gre_b = Button(self.przyciski, text="Wczytaj gre")
        self.w_gre_b.pack(side=TOP)

        self.wybrany_spawn_str = StringVar()
        self.wybrany_spawn_str.set("Czlowiek")

        self.spawn_lista = Frame(self.przyciski, width=200)
        self.spawn_lista.config(background="red")

        self.lewo_b = Button(self.spawn_lista, text="←")
        self.lewo_b.pack(side=BOTTOM)
        self.wybrany_spawn = Label(self.spawn_lista, textvariable=self.wybrany_spawn_str)
        self.wybrany_spawn.pack(side=TOP)
        self.prawo_b = Button(self.spawn_lista, text="→")
        self.prawo_b.pack(side=BOTTOM)
        self.spawn_lista.pack(side=TOP,)

        self.grid_b = Button(self.przyciski, text="Grid")
        self.grid_b.pack(side=TOP)
        self.wyjdz_b = Button(self.przyciski, text="Wyjdz", command=lambda: self.quit_game())
        self.wyjdz_b.pack(side=TOP)

        self.obraz = Canvas(self.okno)
        self.obraz.config(background='green')
        self.obraz.bind("<Button-1>", self.mouse_click)
        self.komunikaty = StringVar()
        self.komunikaty.set("Komunikaty\nBarsz Sosnowskiego zjada mlecz")
        self.widok_komunikaty = Label(self.okno, textvariable=self.komunikaty, width=28, anchor=W)

        self.przyciski.pack(side=RIGHT, fill='y', expand=False)
        self.widok_komunikaty.pack(side=LEFT, fill='y', expand=False)
        self.obraz.pack(side=LEFT, fill='both', expand=True)

    def rysuj(self):
        self.obraz.delete('all')
        self.swiat.rysuj_swiat(self.obraz)
        self.okno.update_idletasks()
        self.okno.update()

    def new_game(self):
        wysokosc = simpledialog.askinteger("Wysokosc", "Podaj wysokosc:", parent=self.okno)
        szerokosc = simpledialog.askinteger("Szerokosc", "Podaj szerokosc:", parent=self.okno)
        populacja = simpledialog.askinteger("Populacja", "Podaj % zapelnienia:", parent=self.okno)
        if wysokosc > 0 and szerokosc > 0 and 0 <= populacja <= 100:
            self.swiat = Swiat(wysokosc, szerokosc)
            self.swiat.dodaj_organizm(Owca(Wspolrzedne(1, 1), self.swiat))
            self.swiat.dodaj_organizm(Owca(Wspolrzedne(3, 3), self.swiat))
            self.swiat.dodaj_organizm(Wilk(Wspolrzedne(8, 8), self.swiat))
            self.swiat.dodaj_organizm(Czlowiek(Wspolrzedne(5, 5), self.swiat))
        else:
            messagebox.showerror("Blad", "Podano bledne dane")

    def quit_game(self):
        self.okno.destroy()
        #self.running = False

    def new_turn(self):
        self.swiat.wykonaj_ture()
        self.swiat.wypisz_komunikaty(self.komunikaty)
        self.rysuj()

    def key_press(self, event):
        self.swiat.zapisz_polecenie(str(event.keysym))
        self.new_turn()

    def mouse_click(self, event):
        self.swiat.wprowadz_organizm(event.x, event.y, 'owca', self.obraz)
        self.rysuj()

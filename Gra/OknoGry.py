from tkinter import *
from Swiat import *


class Okno:
    def __init__(self):
        self.running = True
        self.okno = Tk()
        self.okno.title("Wirtualny Swiat - Adrian Misiak 171600")
        self.okno.minsize(800, 240)
        self.swiat = Swiat(10, 10)

        self.przyciski = Frame(self.okno, width=330, background='yellow')
        self.n_gra_b = Button(self.przyciski, text="Nowa gra", command=lambda: self.new_game(), width=20)
        self.n_gra_b.pack(side=TOP)
        self.n_tura_b = Button(self.przyciski, text="Nowa tura")
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
        print("New game!")

    def quit_game(self):
        self.okno.destroy()
        self.running = False

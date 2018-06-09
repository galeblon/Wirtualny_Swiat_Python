from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
from Swiat import *
import sys
sys.setrecursionlimit(10000)


class Okno:
    index_wyboru = 11

    def __init__(self):
        self.okno = Tk()
        self.okno.title("Wirtualny Swiat - Adrian Misiak 171600")
        self.okno.minsize(800, 240)

        self.okno.bind("<Key>", self.key_press)
        self.okno.bind("<Configure>", self.aktualizuj)

        self.swiat = Swiat(10, 10)

        self.przyciski = Frame(self.okno, width=330, background='yellow')
        self.n_gra_b = Button(self.przyciski, text="Nowa gra", command=lambda: self.new_game(), width=20)
        self.n_gra_b.pack(side=TOP)
        self.n_tura_b = Button(self.przyciski, text="Nowa tura", command=lambda: self.new_turn())
        self.n_tura_b.pack(side=TOP)
        self.z_gre_b = Button(self.przyciski, text="Zapisz gre", command=lambda: self.save_game())
        self.z_gre_b.pack(side=TOP)
        self.w_gre_b = Button(self.przyciski, text="Wczytaj gre", command=lambda: self.load_game())
        self.w_gre_b.pack(side=TOP)

        self.wybrany_spawn_str = StringVar()
        self.wybrany_spawn_str.set("Czlowiek")

        self.spawn_lista = Frame(self.przyciski, width=200)
        self.spawn_lista.config(background="red")

        self.lewo_b = Button(self.spawn_lista, text="←", command=lambda: self.zmien_wybrany(-1))
        self.lewo_b.pack(side=BOTTOM)
        self.wybrany_spawn = Label(self.spawn_lista, textvariable=self.wybrany_spawn_str)
        self.wybrany_spawn.pack(side=TOP)
        self.prawo_b = Button(self.spawn_lista, text="→", command=lambda: self.zmien_wybrany(1))
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
        self.komunikaty.set("Komunikaty:")
        self.widok_komunikaty = Label(self.okno, textvariable=self.komunikaty, width=28, anchor=NW, height=10)

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
            startowe = Wspolrzedne(randint(1, szerokosc), randint(1, wysokosc))
            self.swiat.dodaj_organizm(Czlowiek(startowe, self.swiat))
            licznik_stworzen = 1
            proba = 0
            liczba_organizmow = int(wysokosc*szerokosc*populacja/100)
            max_prob = liczba_organizmow*liczba_organizmow
            while proba < max_prob:
                if licznik_stworzen > liczba_organizmow:
                    proba = max_prob
                startowe = Wspolrzedne(randint(1, szerokosc), randint(1, wysokosc))
                if self.swiat.znajdz_organizm(startowe) is None:
                    self.swiat.dodaj_organizm(self.swiat.stworz_losowy(startowe))
                    licznik_stworzen += 1
                proba += 1
            self.rysuj()
        else:
            messagebox.showerror("Blad", "Podano bledne dane")

    def quit_game(self):
        self.okno.destroy()

    def new_turn(self):
        self.swiat.wykonaj_ture()
        self.swiat.wypisz_komunikaty(self.komunikaty)
        self.rysuj()

    def key_press(self, event):
        self.swiat.zapisz_polecenie(str(event.keysym))
        self.new_turn()

    def mouse_click(self, event):
        self.swiat.wprowadz_organizm(event.x, event.y, self.wybrany_spawn_str.get(), self.obraz)
        self.swiat.wypisz_komunikaty(self.komunikaty)
        self.rysuj()

    def aktualizuj(self, event):
        self.rysuj()

    def zmien_wybrany(self, val):
        self.index_wyboru += val
        if self.index_wyboru < 0:
            self.index_wyboru = 11
        if self.index_wyboru > 11:
            self.index_wyboru = self.index_wyboru % 12
        wybory = {
            0: 'CyberOwca',
            1: 'Owca',
            2: 'Wilk',
            3: 'Zolw',
            4: 'Lis',
            5: 'Antylopa',
            6: 'Trawa',
            7: 'Mlecz',
            8: 'Guarana',
            9: 'WilczeJagody',
            10: 'BarszczSosnowskiego',
            11: 'Czlowiek',
        }
        self.wybrany_spawn_str.set(wybory[self.index_wyboru])

    def save_game(self):
        nazwa_pliku = filedialog.asksaveasfilename(parent=self.okno, title="Gdzie zapisac gre:")
        plik = open(nazwa_pliku, 'w+')
        # plik.write('ayy\n')
        print(nazwa_pliku)
        pass

    def load_game(self):
        pass

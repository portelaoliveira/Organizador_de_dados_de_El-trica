import pandas as pd
import tkinter as tk
from tkinter import Button, Label, Entry
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter import messagebox
import numpy as np
import os


class Tela:
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Organizador de dados de Elétrica")
        self.window.geometry('350x100')

        self.create_screen()

        self.window.mainloop()

    def create_screen(self):

        self.botaoAbrir = Button(
            self.window, text="Abrir arquivo CSV", command=self.read_file_csv)
        self.botaoAbrir.pack()
        self.botaoAbrir.grid(column=1, row=0, pady=15)

        gap_lbl = Label(self.window, text="Espaçamento EL:",
                        font=("Helvetica", 12))
        gap_lbl.grid(column=0, row=2, pady=8)
        self.gap = Entry(self.window, width=11, font=("Helvetica", 12))
        self.gap.grid(column=1, row=2)

    def read_file_csv(self):
        try:
            spacing = float(self.gap.get())

            file_name = askopenfilename(defaultextension=".csv")
            if (os.path.isfile(file_name) and file_name.endswith(".csv")):
                file = pd.read_csv(file_name, header=None)
                df = pd.DataFrame(file)
                df.columns = ['Numerate', 'Eletrodos', 'Long', 'Lat', 'Cota']
                df = df[df['Eletrodos'].str.contains('EL')]
                cota = df["Cota"]
                long = df["Long"]
                lat = df["Lat"]
                lenth = (len(df) * spacing)
                spacing_el = list(np.arange(0, lenth, spacing))
                cota = list(cota)
                long = list(np.round(long, 3))
                lat = list(np.round(lat, 3))
                topography = zip(spacing_el, cota)
                coordinate = zip(spacing_el, long, lat)

                with asksaveasfile(mode="w", defaultextension=".txt") as arquivo:
                    arquivo.write(
                        f'Topography in separeted list\n2\n{len(spacing_el)}\n')
                    lines_topography = (
                        f'{spacing_el}\t{cota}\n' for spacing_el, cota in topography)
                    arquivo.writelines(lines_topography)

                    arquivo.write(
                        f'1\nGlobal Coordinates present\nNumber of coordinate points\n{len(spacing_el)}\nLocal Longitude Latitude\n')
                    lines_coordinate = (
                        f'{spacing_el}\t{long}\t{lat}\n' for spacing_el, long, lat in coordinate)
                    arquivo.writelines(lines_coordinate)

                    arquivo.write(f'0\n0\n0\n0\n')

            else:
                messagebox.showerror(
                    title="Erro", message="Não é um arquivo csv")
                return None
        except:
            messagebox.showerror(
                title="Erro", message="Preencha com um número")

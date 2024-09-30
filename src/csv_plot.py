import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Abre el archivo, devuelve si se pudo abrir y np.array correspondiente
def openfile(filename: str) -> {bool, np.array}:
    try:
        file = open(filename, mode="r")
        dataframe = pd.read_csv(file, sep=',')
    except:
        return (False, None)
    # Eliminar columnas no numéricas, ONE LINER INCOMING!!!!!
    dataframe = dataframe.apply(pd.to_numeric, errors='coerce').dropna(axis=1)
    array = dataframe.to_numpy().transpose()
    print(dataframe)    # Debug
    return (True, array)
    
class PlotData:
    def __init__(self, array: np.array,  root: tk.Widget):
        self.colors = []
        self.n_channels = len(array) // 2
        for i in range(self.n_channels):
            self.colors.append('blue')
        self.array = array
        self.root = root
        self.vdiv = []
        for i in range(0, self.n_channels):
            self.vdiv.append(1.0)
    
    # Grafica el np.array en el tk widget
    def makeplot(self, event=None):
        for widget in self.root.winfo_children():
            widget.destroy()
        fig = plt.Figure()
        self.plot = fig.add_subplot()
        self.plot.grid(True)
        for i in range(0, self.n_channels):
            self.plot.plot(self.array[2*i], (1/self.vdiv[i]) * (self.array[2*i + 1]), self.colors[i])
        self.canvas = FigureCanvasTkAgg(fig, self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH)
        print(self.root.winfo_children())   # Debug

    def updateplot(self, event=None):
        self.plot.clear()
        for i in range(0, self.n_channels):
            self.plot.plot(self.array[2*i], (1/self.vdiv[i]) * (self.array[2*i + 1]), self.colors[i])
        self.plot.grid(True)
        self.canvas.draw()




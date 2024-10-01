from matplotlib.ticker import MultipleLocator
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
import re

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Abre el archivo, devuelve si se pudo abrir y np.array correspondiente
def openfile(filename: str) -> {bool, np.array}:
    try:
        dataframe = pd.read_csv(filename, sep=',')
        print(dataframe.columns.size)
        # Si solo hay una columna, debe ser TSV. Big brain 600 iq move
        if int(dataframe.columns.size) <= 1:
            dataframe = pd.read_csv(filename, sep='\t')
    except:
        return (False, None)
    # Eliminar columnas no numéricas, ONE LINER INCOMING!!!!!
    #dataframe = dataframe.apply(pd.to_numeric, errors='coerce').dropna(axis=1)
    array = dataframe.to_numpy().transpose()
    print(dataframe)    # Debug
    return (True, array)
    
class PlotData:
    def __init__(self, array: np.array,  root: tk.Widget):
        self.vdiv = []
        self.offset = []
        self.colors = []
        self.n_channels = len(array) - 1
        self.array = array
        self.root = root
        for i in range(0, self.n_channels):
            self.colors.append('blue')
            self.vdiv.append(1.0)
            self.offset.append(0.0)
    
    # Grafica el np.array en el tk widget
    def makeplot(self, event=None):
        for widget in self.root.winfo_children():
            widget.destroy()
        fig = plt.Figure()
        self.zoom = 1
        self.lowlimx = min(self.array[0])
        self.highlimx = max(self.array[0])
        self.toffset = 0.0
        self.plot = fig.add_subplot()
        self.plot.set_xlim(self.lowlimx, self.highlimx)
        self.plot.yaxis.set_major_locator(MultipleLocator(1))
        self.plot.grid(True)
        for i in range(0, self.n_channels):
            self.plot.plot(self.array[0], self.offset[i] + (1/self.vdiv[i]) * (self.array[i+1]), self.colors[i])
        self.canvas = FigureCanvasTkAgg(fig, self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH)
        #print(self.root.winfo_children())   # Debug

    def updateplot(self, event=None):
        self.plot.clear()
        self.plot.set_xlim([self.lowlimx / self.zoom, self.highlimx / self.zoom])
        self.plot.yaxis.set_major_locator(MultipleLocator(1))
        for i in range(0, self.n_channels):
            self.plot.plot((self.array[0] - self.toffset), self.offset[i] + (1/self.vdiv[i]) * (self.array[i+1]), self.colors[i])
        self.plot.grid(True)
        self.canvas.draw()


unit_multipliers = {
    'n': 1e-9,  # nano
    'u': 1e-6,  # micro
    'm': 1e-3,  # milli
    's': 1,      # one
}

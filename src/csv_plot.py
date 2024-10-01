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
        #print(dataframe.columns.size)  # Debug
        # Si solo hay una columna, debe ser TSV. Big brain 600 iq move
        if int(dataframe.columns.size) <= 1:
            dataframe = pd.read_csv(filename, sep='\t')
    except:
        return (False, None)
    # Eliminar columnas no numéricas, ONE LINER INCOMING!!!!!
    #dataframe = dataframe.apply(pd.to_numeric, errors='coerce').dropna(axis=1)
    array = dataframe.to_numpy().transpose()
    #print(dataframe)    # Debug
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
        self.delta_t = self.highlimx - self.lowlimx
        self.toffset = 0.0
        self.plot = fig.add_subplot()
        self.plot.set_xlim(self.lowlimx, self.highlimx)
        self.gridy = 1
        self.gridx = "1"
        self.plot.grid(True)
        self.plot.xaxis.set_tick_params(labelbottom=False)
        self.showchannels = []
        self.channel_names = []
        for i in range(self.n_channels):
            self.showchannels.append(True)
            self.channel_names.append("")
        self.canvas = FigureCanvasTkAgg(fig, self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH)
        self.updateplot()
        #print(self.root.winfo_children())   # Debug

    def updateplot(self, event=None):
        self.plot.clear()

        (gridx_base, gridx_exp) = get_unit(self.gridx)
        gridx = gridx_base * gridx_exp
        #print(gridx_base * gridx_exp)  # Debug
        self.plot.yaxis.set_major_locator(MultipleLocator(self.gridy))
        self.plot.xaxis.set_major_locator(MultipleLocator(gridx))
        self.plot.set_xlim([self.lowlimx / self.zoom, self.highlimx / self.zoom])
        for i in range(0, self.n_channels):
            if self.showchannels[i]:
                self.plot.plot((self.array[0] - self.toffset), 
                           self.offset[i] + (1/self.vdiv[i]) * (self.array[i+1]), self.colors[i]
                           , label=self.channel_names[i])
                if self.channel_names[i] != "":
                    leg = self.plot.legend() 
        self.plot.grid(True)
        self.canvas.draw()

def get_unit(val):
    if val[-1].isalpha():
        base = float(val[0:-1])
        exp = unit_multipliers[val[-1]]
    else:
        base = float(val)
        exp = 1
    return (base, exp)

unit_multipliers = {
    'n': 1.0E-9,  # nano
    'u': 1.0E-6,  # micro
    'm': 1E-3,  # milli
}
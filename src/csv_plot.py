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
    dataframe = dataframe.transpose().apply(pd.to_numeric, errors='coerce').dropna(axis=1).transpose()
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
        self.delta_y = []
        self.cursor_delta = []
        self.cursor1_v = []
        self.cursor2_v = []
        self.min = []
        self.toffset = 0.0
        self.plot = fig.add_subplot()
        self.plot.set_xlim(self.lowlimx, self.highlimx)
        self.gridy = 1
        self.gridx = "1"
        self.plot.grid(True)
        self.plot.xaxis.set_tick_params(labelbottom=False)
        self.showchannels = []
        self.channel_names = []
        self.cursor_chk = []
        self.cursor1 = []
        self.cursor2 = []
        self.tcursor1 = 0.0
        self.tcursor2 = 0.0
        self.tcursor_chk = False
        self.tcursor1_t = 0.0
        self.tcursor2_t = 0.0
        self.tcursor_delta = 0.0
        self.title = ""
        self.xtitle = ""
        self.ytitle = ""
        for i in range(self.n_channels):
            self.showchannels.append(True)
            self.channel_names.append(self.array[i][1])
            self.min.append(min(self.array[i+1]))
            self.delta_y.append(max(self.array[i+1]) - self.min[i])
            self.cursor_delta.append(0.0)
            self.cursor1_v.append(0.0)
            self.cursor2_v.append(0.0)
        self.canvas = FigureCanvasTkAgg(fig, self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH)
        #self.updateplot()
        #print(self.root.winfo_children())   # Debug

    def updateplot(self, event=None):
        self.plot.clear()

        (gridx_base, gridx_exp) = get_unit(self.gridx)
        gridx = gridx_base * gridx_exp
        #print(gridx_base * gridx_exp)  # Debug
        self.plot.yaxis.set_major_locator(MultipleLocator(self.gridy))
        self.plot.xaxis.set_major_locator(MultipleLocator(gridx))
        self.plot.set_xlim([self.lowlimx / self.zoom, self.highlimx / self.zoom])
        self.plot.set_title(self.title)
        self.plot.set_xlabel(self.xtitle)
        self.plot.set_ylabel(self.ytitle)
        for i in range(0, self.n_channels):
            if self.showchannels[i]:
                self.plot.plot((self.array[0] - self.toffset), 
                           self.offset[i] + (1/self.vdiv[i]) * (self.array[i+1]), self.colors[i]
                           , label=self.channel_names[i])
                if self.cursor_chk[i] == True:
                    self.cursor1_v[i] = self.offset[i] + (1/self.vdiv[i]) * (self.min[i] + self.delta_y[i] * self.cursor1[i])
                    self.cursor2_v[i] = self.offset[i] + (1/self.vdiv[i]) * (self.min[i] + self.delta_y[i] * self.cursor2[i])
                    self.plot.axhline(y=self.cursor1_v[i], color=self.colors[i], linestyle=':')
                    self.plot.axhline(y=self.cursor2_v[i], color=self.colors[i], linestyle='--')
                    self.cursor_delta[i] = self.cursor1_v[i] - self.cursor2_v[i]
                if self.channel_names[i] != "":
                    self.plot.legend() 
        if self.tcursor_chk == True:
            self.tcursor1_t = (self.lowlimx + self.toffset + self.delta_t * self.tcursor1) / self.zoom
            self.tcursor2_t = (self.lowlimx + self.toffset +  self.delta_t * self.tcursor2) / self.zoom
            self.tcursor_delta = self.tcursor1_t - self.tcursor2_t
            self.plot.axvline(x=self.tcursor1_t, linestyle=':', color='black')
            self.plot.axvline(x=self.tcursor2_t, linestyle='--', color='black')
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
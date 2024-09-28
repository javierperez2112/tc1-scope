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
        dataframe = pd.read_csv(file, sep='\t')
    except:
        return (False, None)
    array = dataframe.to_numpy().transpose()
    return (True, array)

# Grafica el np.array en el tk widget
def graphfile(array: np.array, root: tk.Widget):
    fig = plt.Figure()
    plot1 = fig.add_subplot()
    for i in range(1,len(array)):
        plot1.plot(array[0], array[i])
    graph1 = FigureCanvasTkAgg(fig, root)
    graph1.get_tk_widget().pack()
    


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def openfile(filename: str) -> np.array:
    try:
        file = open(filename, mode="r")
        dataframe = pd.read_csv(file, sep='\t')
    except:
        return None
    array = dataframe.to_numpy().transpose()
    return array

def graphfile(array: np.array, root: tk.Widget):
    fig = plt.Figure()
    plot1 = fig.add_subplot(111)
    for i in range(1,len(array)):
        plot1.plot(array[0], array[i])
    graph1 = FigureCanvasTkAgg(fig, root)
    graph1.get_tk_widget().pack()
    


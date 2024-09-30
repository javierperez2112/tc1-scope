import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv_plot

# Abre navegador para buscar archivo
def browse_files(event):
    filename = filedialog.askopenfilename(initialdir = ".",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
    ent_filename.delete(0, tk.END)
    ent_filename.insert(0, filename)

# Busca el archivo del campo de texto
def search_entry(event):
    search(ent_filename.get())
    
# Intenta abrir el archivo
def search(filename):
    # Si se encuentra el archivo, pasa a pantalla principal
    (fileopen, array) = csv_plot.openfile(filename=filename)
    if fileopen:    # Si se puede abrir, pasa a pantalla principal y crea canales y config
        #frm_welcome.destroy()
        #frm_board.pack(fill=tk.BOTH, expand=True)
        frm_welcome.destroy()
        frm_board.pack(fill=tk.BOTH)
        window.resizable(width=True, height=True)
        data = csv_plot.PlotData(array, frm_screen)
        data.updateplot()
        (chan_vdiv, chan_color) = createchannels(data.n_channels, frm_board)
        btn_update.config(command = lambda: update(data, chan_vdiv, chan_color))
        window.title("TC1-SCOPE - " + os.path.basename(filename))
    else:
        lbl_file.config(text="File not found or unable to open.")

# Crea canales acorde al .csv y devuelve los widgets para leer
def createchannels(n_channels: int, root: tk.Widget) -> tuple[list[type[tk.Spinbox]], list[type[ttk.Combobox]]]:
    chan_vdiv = []
    chan_color = []
    for i in range(0, n_channels):
        panel = tk.Frame(master=root)
        lbl_channel = tk.Label(text=("Channel " + str(i+1) + "\nV/div"), master=panel)
        spb_vdiv = tk.Spinbox(from_=0.1, to=10, increment=0.1, master=panel)
        spb_vdiv.delete(0, tk.END)
        spb_vdiv.insert(0,1)
        lbl_color = tk.Label(text="Color", master=panel)
        cbb_color = ttk.Combobox(values=["blue","green","red","cyan","magenta","yellow","black","white"], state='readonly', master=panel)
        cbb_color.delete(0,tk.END)
        cbb_color.insert(0,"blue")

        lbl_channel.pack()
        spb_vdiv.pack()
        lbl_color.pack()
        cbb_color.pack()
        panel.pack(side=tk.LEFT)
        chan_vdiv.append(spb_vdiv)
        chan_color.append(cbb_color)
    return (chan_vdiv, chan_color)

def update(data: csv_plot.PlotData, chan_vdiv: list[type[tk.Spinbox]], chan_color: list[type[ttk.Combobox]]):
    for i in range(0,data.n_channels):
        data.vdiv[i] = float(tk.Spinbox.get(chan_vdiv[i]))
        data.colors[i] = chan_color[i].get()
    data.updateplot()

window = tk.Tk()
#window.resizable(width=False, height=False)
window.title("TC1-SCOPE")
window.pack_propagate(True)

# Screen frames
frm_screen = tk.Frame(width=610, height=410, bg="black", borderwidth=3, relief=tk.SUNKEN)
frm_welcome = tk.Frame(borderwidth=3, relief=tk.RAISED)
frm_board = tk.Frame(width=610, height = 500, borderwidth=3, relief=tk.RAISED)
frm_board.pack_propagate(True)

# Welcome screen
lbl_file = tk.Label(text="Select file", master=frm_welcome)
ent_filename = tk.Entry(master=frm_welcome)
ent_filename.bind("<Return>", search_entry)
btn_browse = tk.Button(text="Browse", master=frm_welcome)
btn_entry = tk.Button(text="Open", master=frm_welcome)
btn_browse.bind("<Button-1>", browse_files)
btn_entry.bind("<Button-1>", search_entry)
filefound = False

lbl_file.pack()
ent_filename.pack()
btn_entry.pack()
btn_browse.pack()

# Main screen
btn_update = tk.Button(text="Update", master=frm_board)
btn_update.bind("<Button-1>")
btn_update.pack(side=tk.RIGHT)

# Layout
#frm_screen.pack(fill=tk.BOTH)
#frm_welcome.pack(fill=tk.BOTH)
frm_screen.pack(fill=tk.BOTH)
frm_welcome.pack(fill=tk.BOTH)

# Start the event loop.
window.mainloop()
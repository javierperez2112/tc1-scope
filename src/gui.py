import tkinter as tk
from tkinter import filedialog
import csv_plot

def browse_files(event):
    filename = filedialog.askopenfilename(initialdir = ".",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
    search(filename=filename)

def browse_entry(event):
    search(ent_filename.get())
    
def search(filename):
    # Si se encuentra el archivo, pasa a pantalla principal
    (fileopen, array) = csv_plot.openfile(filename=filename)
    if fileopen:
        #frm_welcome.destroy()
        #frm_board.pack(fill=tk.BOTH, expand=True)
        pwindow.remove(frm_welcome)
        pwindow.add(frm_board)
        window.minsize(width =100, height=310)
        window.resizable(width=True, height=True)
        csv_plot.graphfile(array=array, root=frm_screen)
    else:
        lbl_file.config(text="File not found or unable to open.")

window = tk.Tk()
window.resizable(width=False, height=False)
window.title("TC1-SCOPE")

pwindow = tk.PanedWindow(master=window, orient=tk.VERTICAL, borderwidth=0, showhandle=False, sashwidth=2)
pwindow.pack(fill=tk.BOTH)

# Screen frames
frm_screen = tk.Frame(width=610, height=410, bg="black", borderwidth=3, relief=tk.SUNKEN, master=pwindow)
frm_welcome = tk.Frame(borderwidth=3, relief=tk.RAISED, master=pwindow)
frm_board = tk.Frame(width = 610, height = 310, borderwidth=3, relief=tk.RAISED, master=pwindow)

# Welcome screen
lbl_file = tk.Label(text="Select file", master=frm_welcome)
ent_filename = tk.Entry(master=frm_welcome)
ent_filename.bind("<Return>", browse_entry)
btn_browse = tk.Button(text="Browse", master=frm_welcome)
btn_entry = tk.Button(text="Open", master=frm_welcome)
btn_browse.bind("<Button-1>", browse_files)
btn_entry.bind("<Button-1>", browse_entry)
filefound = False

lbl_file.pack()
ent_filename.pack()
btn_entry.pack()
btn_browse.pack()

# Main screen


# Layout
#frm_screen.pack(fill=tk.BOTH)
#frm_welcome.pack(fill=tk.BOTH)
pwindow.add(frm_screen)
pwindow.add(frm_welcome)

# Start the event loop.
window.mainloop()
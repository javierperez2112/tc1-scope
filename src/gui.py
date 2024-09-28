import tkinter as tk
import csv_plot


def search(event):
    # Si se encuentra el archivo, pasa a pantalla principal
    array = csv_plot.openfile(ent_filename.get())
    if array.all() != None:
        frm_welcome.destroy()
        frm_board.pack(fill=tk.BOTH)
        csv_plot.graphfile(array=array, root=frm_screen)
    else:
        lbl_file.config(text="File not found or unable to open.")

window = tk.Tk()
window.resizable(width=False, height=False)
window.title("TC1-SCOPE")

frm_screen = tk.Frame(width=610, height=410, bg="black", borderwidth=5, relief=tk.SUNKEN, master=window)
frm_welcome = tk.Frame(borderwidth=5, relief=tk.RAISED, master=window)
frm_board = tk.Frame(width = 610, height = 310, borderwidth=5, relief=tk.RAISED, master=window)
frm_board.grid_propagate(0)

# Welcome screen
lbl_file = tk.Label(text="Input filename", master=frm_welcome)
ent_filename = tk.Entry(master=frm_welcome)
btn_searchfile = tk.Button(text="Search", master=frm_welcome)
btn_searchfile.bind("<Button-1>", search)
filefound = False

lbl_file.pack()
ent_filename.pack()
btn_searchfile.pack()

# Main screen


# Layout
#frm_screen.grid(row=0,column=0,sticky="nsew")
#frm_board.grid(row=1,column=0, sticky="nsew")
frm_screen.pack(fill=tk.BOTH)
frm_welcome.pack(fill=tk.BOTH)

# Start the event loop.
window.mainloop()
import tkinter as tk

window = tk.Tk()
#window.resizable(width=False, height=False)
window.title("TC1-SCOPE")

frm_screen = tk.Frame(width=610, height=410, bg="black", borderwidth=5, relief=tk.SUNKEN, master=window)
frm_board = tk.Frame(width = 610, height = 310, borderwidth=5, relief=tk.RAISED, master=window)
frm_board.grid_propagate(0)

for i in range(3):
    frm_board.columnconfigure(i, weight=1)
    frm_board.rowconfigure(i, weight=1)
    frame = tk.Frame(master=frm_board, borderwidth=3, relief=tk.SUNKEN)
    frame.pack_propagate(1)
    button = tk.Button(text=("Button " + str(1+i)), master=frame)
    button.pack()
    frame.grid(row=0, column=i, sticky="nsew")


# Layout
#frm_screen.grid(row=0,column=0,sticky="nsew")
#frm_board.grid(row=1,column=0, sticky="nsew")

frm_screen.pack(fill=tk.BOTH)
frm_board.pack(fill=tk.BOTH)

# Start the event loop.
window.mainloop()
import os
import tkinter as tk
from tkinter import ttk, filedialog
import csv_plot

class TC1ScopeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TC1-SCOPE")
        self.root.pack_propagate(True)

        # Initialize frames
        self.frm_screen = tk.Frame(width=610, height=410, bg="black", borderwidth=3, relief=tk.SUNKEN)
        self.frm_welcome = tk.Frame(borderwidth=3, relief=tk.RAISED)
        self.frm_board = tk.Frame(width=610, height=500, borderwidth=3, relief=tk.RAISED)
        self.frm_board.pack_propagate(True)

        # Initialize widgets
        self.ent_filename = tk.Entry(master=self.frm_welcome)
        self.lbl_file = tk.Label(text="Select file", master=self.frm_welcome)
        self.btn_browse = tk.Button(text="Browse", master=self.frm_welcome)
        self.btn_entry = tk.Button(text="Open", master=self.frm_welcome)
        self.btn_update = tk.Button(text="Update", master=self.frm_board)

        # Pack the welcome screen widgets
        self.lbl_file.pack()
        self.ent_filename.pack()
        self.btn_entry.pack()
        self.btn_browse.pack()

        # Bind events to buttons
        self.root.bind("<Return>", self.search_entry)
        self.btn_browse.bind("<Button-1>", self.browse_files)
        self.btn_entry.bind("<Button-1>", self.search_entry)

        # Layout
        self.frm_screen.pack(fill=tk.BOTH)
        self.frm_welcome.pack(fill=tk.BOTH)

    def browse_files(self, event):
        filename = filedialog.askopenfilename(initialdir=".", title="Select a File",
                                              filetypes=(("Text files", "*.csv*"), ("all files", "*.*")))
        self.ent_filename.delete(0, tk.END)
        self.ent_filename.insert(0, filename)

    def search_entry(self, event):
        filename = self.ent_filename.get()
        self.search(filename)

    def search(self, filename):
        # Try to open the file
        fileopen, array = csv_plot.openfile(filename=filename)
        if fileopen:
            # Move from welcome screen to main board and setup plot
            self.frm_welcome.destroy()
            self.frm_board.pack(fill=tk.BOTH)
            self.root.resizable(width=True, height=True)

            # Initialize the data and create channel controls
            self.data = csv_plot.PlotData(array, self.frm_screen)
            self.data.makeplot()
            self.chan_vdiv, self.chan_color = self.create_channels(self.data.n_channels)
            self.root.bind("<Return>", self.update_channels)
            
            # Set update button action
            self.btn_update.config(command=self.update_channels)
            self.btn_update.pack(side=tk.RIGHT)
            self.root.title(f"TC1-SCOPE - {os.path.basename(filename)}")
        else:
            self.lbl_file.config(text="File not found or unable to open.")

    def create_channels(self, n_channels):
        chan_vdiv = []
        chan_color = []
        for i in range(n_channels):
            panel = tk.Frame(master=self.frm_board)

            lbl_channel = tk.Label(text=f"Channel {i + 1}\nV/div", master=panel)
            spb_vdiv = tk.Spinbox(from_=0.1, to=10, increment=0.1, master=panel)
            spb_vdiv.delete(0, tk.END)
            spb_vdiv.insert(0, 1)
            spb_vdiv.config(command=self.update_channels)

            lbl_color = tk.Label(text="Color", master=panel)
            cbb_color = ttk.Combobox(values=["blue", "green", "red", "cyan", "magenta", "orange", "black", "white"],
                                     state='readonly', master=panel)
            cbb_color.set("blue")
            cbb_color.bind("<<ComboboxSelected>>", self.update_channels)

            # Pack widgets
            lbl_channel.pack()
            spb_vdiv.pack()
            lbl_color.pack()
            cbb_color.pack()
            panel.pack(side=tk.LEFT)

            chan_vdiv.append(spb_vdiv)
            chan_color.append(cbb_color)

        return chan_vdiv, chan_color

    def update_channels(self, event=0):
        for i in range(self.data.n_channels):
            self.data.vdiv[i] = float(self.chan_vdiv[i].get())
            self.data.colors[i] = self.chan_color[i].get()
        self.data.updateplot()

# Start the application
if __name__ == "__main__":
    window = tk.Tk()
    app = TC1ScopeApp(window)
    window.mainloop()

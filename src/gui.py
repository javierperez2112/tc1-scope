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
        self.frm_right = tk.Frame(master=self.frm_board)

        # Initialize widgets
        self.ent_filename = tk.Entry(master=self.frm_welcome)
        self.lbl_file = tk.Label(text="Select file", master=self.frm_welcome)
        self.btn_browse = tk.Button(text="Browse", master=self.frm_welcome)
        self.btn_entry = tk.Button(text="Open", master=self.frm_welcome)

        self.lbl_zoom = tk.Label(text="Time zoom", master=self.frm_right)
        self.spb_zoom = tk.Spinbox(master=self.frm_right)
        self.spb_zoom.config(from_=1, to=100)

        self.lbl_toffset = tk.Label(text="Time offset",master=self.frm_right)
        self.lbl_coarseoffset = tk.Label(text="Coarse", master=self.frm_right)
        self.scl_toffset = tk.Scale(master=self.frm_right, resolution=0.1, orient=tk.HORIZONTAL, showvalue=False)
        self.lbl_fineoffset = tk.Label(text="Fine", master=self.frm_right)
        self.scl_toffsetfine = tk.Scale(master=self.frm_right, resolution=0.1, orient=tk.HORIZONTAL, showvalue=False)
        self.btn_offsetzero = tk.Button(text="Reset offset", master=self.frm_right)

        # Pack the welcome screen widgets
        self.lbl_file.pack()
        self.ent_filename.pack()
        self.btn_entry.pack()
        self.btn_browse.pack()

        # Pack static main screen widgets
        self.lbl_zoom.pack()
        self.spb_zoom.pack()
        self.lbl_toffset.pack()
        self.lbl_coarseoffset.pack()
        self.scl_toffset.pack()
        self.lbl_fineoffset.pack()
        self.scl_toffsetfine.pack()
        self.btn_offsetzero.pack()

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
            self.spb_zoom.config(command=self.update_channels)
            self.scl_toffset.config(command=self.update_channels)
            self.scl_toffsetfine.config(command=self.update_channels)
            self.btn_offsetzero.bind("<Button-1>", self.reset_offset)
            delta_t = self.data.highlimx - self.data.lowlimx
            self.scl_toffset.config(from_=-delta_t, to=delta_t, resolution=-1)
            self.scl_toffsetfine.config(from_=-delta_t, to=delta_t, resolution=-1)
            self.frm_right.pack(side=tk.RIGHT)
            self.create_channels(self.data.n_channels)
            self.root.bind("<Return>", self.update_channels)
            self.root.title(f"TC1-SCOPE - {os.path.basename(filename)}")
        else:
            self.lbl_file.config(text="File not found or unable to open.")

    def create_channels(self, n_channels):
        chan_vdiv = []
        chan_offset = []
        chan_color = []
        chan_title = []
        for i in range(n_channels):
            panel = tk.Frame(master=self.frm_board)

            lbl_channel = tk.Label(text=f"Channel {i + 1}", master=panel, fg="white", bg="blue")
            lbl_vdiv = tk.Label(text="V/div", master=panel)
            spb_vdiv = tk.Spinbox(from_=0.01, to=100, increment=0.1, master=panel)
            spb_vdiv.delete(0, tk.END)
            spb_vdiv.insert(0, "1.0")
            spb_vdiv.config(command=self.update_channels)

            lbl_offset = tk.Label(text="V offset", master=panel)
            spb_offset = tk.Spinbox(from_=-10, to=10, increment=0.1, master=panel)
            spb_offset.config(command=self.update_channels)
            spb_offset.delete(0, tk.END)
            spb_offset.insert(0, "0.0")

            lbl_color = tk.Label(text="Color", master=panel)
            cbb_color = ttk.Combobox(values=["blue", "green", "red", "gold", "magenta", "orange", "black", "purple"],
                                     state='readonly', master=panel)
            cbb_color.set("blue")
            cbb_color.bind("<<ComboboxSelected>>", self.update_channels)

            # Pack widgets
            lbl_channel.pack()
            lbl_vdiv.pack()
            spb_vdiv.pack()
            lbl_offset.pack()
            spb_offset.pack()
            lbl_color.pack()
            cbb_color.pack()
            panel.pack(side=tk.LEFT)

            chan_vdiv.append(spb_vdiv)
            chan_offset.append(spb_offset)
            chan_color.append(cbb_color)
            chan_title.append(lbl_channel)
        self.chan_vdiv = chan_vdiv
        self.chan_offset = chan_offset
        self.chan_color = chan_color
        self.chan_title = chan_title
    
    def reset_offset(self, event):
        self.scl_toffset.set(0)
        self.scl_toffsetfine.set(0)

    def update_channels(self, event=0):
        for i in range(self.data.n_channels):
            if float(self.chan_vdiv[i].get()) <= 0.1:
                self.chan_vdiv[i].config(increment=0.01)
            else:
                self.chan_vdiv[i].config(increment=0.1)

            self.data.vdiv[i] = float(self.chan_vdiv[i].get())
            self.data.offset[i] = float(self.chan_offset[i].get())
            self.data.colors[i] = self.chan_color[i].get()
            self.chan_title[i].config(bg=self.chan_color[i].get())
        self.data.zoom = float(self.spb_zoom.get())
        self.data.toffset = self.scl_toffset.get() + self.scl_toffsetfine.get()/50
        self.data.updateplot()

# Start the application
if __name__ == "__main__":
    window = tk.Tk()
    app = TC1ScopeApp(window)
    window.mainloop()

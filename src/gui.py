import os
import tkinter as tk
from tkinter import ttk, filedialog
import csv_plot

unit_inverses = {
    '' : '',
    'm' : 'k',
    'u' : 'M',
    'n' : 'G'
}

class TC1ScopeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TC1-SCOPE")
        self.root.pack_propagate(True)

        # Initialize frames
        self.pwindow = tk.PanedWindow(master=self.root)
        self.frm_screen = tk.Frame(width=610, height=410, bg="black", borderwidth=3, relief=tk.SUNKEN)
        self.frm_welcome = tk.Frame(borderwidth=3, relief=tk.RAISED)
        self.frm_board = tk.Frame(width=610, height=500, borderwidth=3, relief=tk.RAISED)
        #self.frm_board.pack_propagate(True)
        self.frm_titles = tk.Frame(master=self.frm_board)
        self.frm_time = tk.Frame(master=self.frm_board)
        self.frm_grid = tk.Frame(master=self.frm_board)
        self.frm_cursor = tk.Frame(master=self.frm_board)

        # Initialize widgets
        # Welcome
        self.ent_filename = tk.Entry(master=self.frm_welcome)
        self.lbl_file = tk.Label(text="Select file", master=self.frm_welcome)
        self.btn_browse = tk.Button(text="Browse", master=self.frm_welcome)
        self.btn_entry = tk.Button(text="Open", master=self.frm_welcome)
        #Time
        self.lbl_zoom = tk.Label(text="Time zoom", master=self.frm_time)
        self.spb_zoom = tk.Spinbox(master=self.frm_time)
        self.spb_zoom.config(from_=1, to=100)
        self.lbl_toffset = tk.Label(text="Time offset",master=self.frm_time)
        self.lbl_coarseoffset = tk.Label(text="Coarse", master=self.frm_time)
        self.scl_toffset = tk.Scale(master=self.frm_time, resolution=0.1, orient=tk.HORIZONTAL, showvalue=False, length=200)
        self.lbl_fineoffset = tk.Label(text="Fine", master=self.frm_time)
        self.scl_toffsetfine = tk.Scale(master=self.frm_time, resolution=0.1, orient=tk.HORIZONTAL, showvalue=False, length=200)
        self.btn_offsetzero = tk.Button(text="Reset offset", master=self.frm_time)
        #Titles
        self.lbl_title = tk.Label(text="Title", master=self.frm_titles)
        self.ent_title = tk.Entry(master=self.frm_titles)
        self.lbl_xtitle = tk.Label(text="X axis title", master=self.frm_titles)
        self.ent_xtitle = tk.Entry(master=self.frm_titles)
        self.lbl_ytitle = tk.Label(text="Y axis title", master=self.frm_titles)
        self.ent_ytitle = tk.Entry(master=self.frm_titles)
        self.xunits = tk.BooleanVar(value=False)
        self.chk_xunits = tk.Checkbutton(text="X units", master=self.frm_titles, onvalue=True, offvalue=False, variable=self.xunits)
        self.chk_xunits.config(command=self.update_channels)
        self.yunits = tk.BooleanVar(value=False)
        self.chk_yunits = tk.Checkbutton(text="Y units", master=self.frm_titles, onvalue=True, offvalue=False, variable=self.yunits)
        self.chk_yunits.config(command=self.update_channels)
        self.xymode = tk.BooleanVar(value=False)
        self.chk_xymode = tk.Checkbutton(text="XY mode", master=self.frm_titles, onvalue=True, offvalue=False, variable=self.xymode)
        self.chk_xymode.config(command=self.update_channels)
        # Grid
        self.lbl_gridx = tk.Label(text="X grid separation (s)", master=self.frm_grid)
        self.spb_gridx = tk.Spinbox(master=self.frm_grid, state='readonly')
        gridx_values = ['10n','25n','50n','100n','250n','500n',
                        '1u','5u','10u','25u','50u','100u','250u','500u',
                        '1m','5m','10m','25m','50m','100m','250m','500m','1','5','10']

        self.spb_gridx.config(values=gridx_values)
        self.lbl_smalltime = tk.Label(text="Time tick too small!", fg="red", master=self.frm_grid)
        self.lbl_gridy = tk.Label(text="Y grid separation (V)", master=self.frm_grid)
        self.spb_gridy = tk.Spinbox(master=self.frm_grid, from_=0.5, to=10, increment=0.5)
        self.spb_gridy.delete(0,tk.END)
        self.spb_gridy.insert(0,1.0)
        self.tcursor = tk.BooleanVar(value=False)
        self.chk_tcursor = tk.Checkbutton(master=self.frm_grid, text="Time cursor", variable=self.tcursor, onvalue=True, offvalue=False)
        self.chk_tcursor.config(command=self.update_channels)
        self.scl_tcursor1 = tk.Scale(master=self.frm_grid, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, showvalue=0)
        self.scl_tcursor1.config(command=self.update_channels)
        self.scl_tcursor2 = tk.Scale(master=self.frm_grid, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, showvalue=0)
        self.scl_tcursor2.config(command=self.update_channels)
        self.tcursor_info = tk.StringVar()
        self.lbl_tcursor = tk.Label(master=self.frm_grid, textvariable=self.tcursor_info)

        # Pack the welcome screen widgets
        self.lbl_file.pack()
        self.ent_filename.pack()
        self.btn_entry.pack()
        self.btn_browse.pack()

        # Pack static main screen widgets
        # Time
        self.lbl_zoom.pack()
        self.spb_zoom.pack()
        self.lbl_toffset.pack()
        self.lbl_coarseoffset.pack()
        self.scl_toffset.pack()
        self.lbl_fineoffset.pack()
        self.scl_toffsetfine.pack()
        self.btn_offsetzero.pack()
        # Titles
        self.lbl_title.pack()
        self.ent_title.pack()
        self.lbl_xtitle.pack()
        self.ent_xtitle.pack()
        self.lbl_ytitle.pack()
        self.ent_ytitle.pack()
        self.chk_xunits.pack()
        self.chk_yunits.pack()
        # Grid
        self.lbl_gridx.pack()
        self.spb_gridx.pack()
        self.lbl_smalltime.pack()
        self.lbl_gridy.pack()
        self.spb_gridy.pack()
        self.chk_tcursor.pack()
        self.scl_tcursor1.pack()
        self.scl_tcursor2.pack()
        self.lbl_tcursor.pack()

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
            self.scl_toffset.config(from_=-self.data.delta_t, to=self.data.delta_t, resolution=self.data.delta_t/1000)
            self.scl_toffsetfine.config(from_=-self.data.delta_t, to=self.data.delta_t, resolution=self.data.delta_t/1000)
            self.frm_time.pack(side=tk.RIGHT, expand=tk.YES)
            self.frm_grid.pack(side=tk.RIGHT, expand=tk.YES)
            self.frm_titles.pack(side=tk.RIGHT, expand=tk.YES)
            self.frm_cursor.pack(side=tk.BOTTOM, expand=tk.YES)
            self.spb_gridy.config(command=self.update_channels)
            self.spb_gridx.config(command=self.update_channels)
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
        chan_check = []
        chan_cursor_chk = []
        chan_cursor1 = []
        chan_cursor2 = []
        chan_cursorinfo = []
        colors = ["blue", "red", "green", "gold", "magenta", "orange", "black", "purple"]
        if n_channels == 2:
            self.chk_xymode.pack()
        for i in range(n_channels):
            panel = tk.Frame(master=self.frm_board)

            frm_chk = tk.Frame(master=panel)
            chk_var = tk.BooleanVar(value=True)
            chk_channel = tk.Checkbutton(master=frm_chk, variable=chk_var, onvalue=True, offvalue=False)
            chk_channel.config(command=self.update_channels)
            ent_channel = tk.Entry(master=frm_chk, fg="white")
            ent_channel.insert(0,f"Channel {i + 1}")
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
            cbb_color = ttk.Combobox(values=colors,
                                     state='readonly', master=panel)
            cbb_color.set(colors[i])
            #cbb_color.set("blue")
            cbb_color.bind("<<ComboboxSelected>>", self.update_channels)

            cursor_var = tk.BooleanVar(value=False)
            chk_cursor = tk.Checkbutton(text=f"Cursor {i+1}", master=panel, variable=cursor_var, onvalue=True, offvalue=False)
            chk_cursor.config(command=self.update_channels)
            spb_cursor1 = tk.Scale(master=panel, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, showvalue=0)
            spb_cursor1.config(command=self.update_channels)
            #spb_cursor1.delete(0,tk.END)
            #spb_cursor1.insert(0,0.0)
            spb_cursor2 = tk.Scale(master=panel, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, showvalue=0)
            spb_cursor2.config(command=self.update_channels)
            #spb_cursor2.delete(0,tk.END)
            #spb_cursor2.insert(0,0.0)
            stringvar = tk.StringVar()
            lbl_cursor = tk.Label(textvariable=stringvar, master=panel)

            # Pack widgets
            chk_channel.pack(side=tk.LEFT)
            ent_channel.pack(side=tk.LEFT)
            frm_chk.pack()
            lbl_vdiv.pack()
            spb_vdiv.pack()
            lbl_offset.pack()
            spb_offset.pack()
            lbl_color.pack()
            cbb_color.pack()
            chk_cursor.pack()
            spb_cursor1.pack()
            spb_cursor2.pack()
            lbl_cursor.pack()
            panel.pack(side=tk.LEFT, expand=tk.YES)

            chan_vdiv.append(spb_vdiv)
            chan_offset.append(spb_offset)
            chan_color.append(cbb_color)
            chan_title.append(ent_channel)
            chan_check.append(chk_var)
            chan_cursor_chk.append(cursor_var)
            chan_cursor1.append(spb_cursor1)
            chan_cursor2.append(spb_cursor2)
            chan_cursorinfo.append(stringvar)
            self.data.cursor_chk.append(None)
            self.data.cursor1.append(0.0)
            self.data.cursor2.append(0.0)
        self.chan_vdiv = chan_vdiv
        self.chan_offset = chan_offset
        self.chan_color = chan_color
        self.chan_title = chan_title
        self.chan_check = chan_check
        self.chan_cursor_chk = chan_cursor_chk
        self.chan_cursor1 = chan_cursor1
        self.chan_cursor2 = chan_cursor2
        self.chan_cursorinfo = chan_cursorinfo
        #self.spb_cursorx1.config(from_=0, to=self.data.delta_t, increment=self.data.delta_t/1000.0)
        #self.spb_cursorx2.config(from_=0, to=self.data.delta_t, increment=self.data.delta_t/1000.0)
        self.update_channels()
    
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
            self.data.showchannels[i] = self.chan_check[i].get()
            self.data.channel_names[i] = self.chan_title[i].get()
            self.chan_title[i].config(bg=self.chan_color[i].get())
            self.data.cursor_chk[i] = self.chan_cursor_chk[i].get()
            self.data.cursor1[i] = float(self.chan_cursor1[i].get())
            self.data.cursor2[i] = float(self.chan_cursor2[i].get())
        self.data.zoom = float(self.spb_zoom.get())
        self.data.toffset = (self.scl_toffset.get() + self.scl_toffsetfine.get() / 50)*self.data.zoom ###
        self.data.gridy = float(self.spb_gridy.get())
        self.data.title = self.ent_title.get()
        self.data.xtitle = self.ent_xtitle.get()
        self.data.ytitle = self.ent_ytitle.get()
        
        self.data.tcursor_chk = self.tcursor.get()
        self.data.tcursor1 = float(self.scl_tcursor1.get())
        self.data.tcursor2 = float(self.scl_tcursor2.get())

        unit_base, unit_exp = csv_plot.get_unit(self.spb_gridx.get())
        ticks_sep = unit_base * unit_exp

        if ((self.data.delta_t / ticks_sep) / self.data.zoom) <= 100:
            self.data.gridx = self.spb_gridx.get()
            self.lbl_smalltime.config(text="")
        else:
            self.data.gridx = "100000"
            self.lbl_smalltime.config(text="Time tick too small!")
        
        self.data.xymode = self.xymode.get()
        

        unit = self.data.gridx[-1]
        if unit.isnumeric():
            unit = ""
        funit = unit_inverses[unit]
        if self.xunits.get() == True:
            if not self.xymode.get():
                self.data.xtitle = self.ent_xtitle.get() + f" ({unit}s)"
            else:
                self.data.xtitle = self.ent_xtitle.get() + f" ({unit}V)"
            
        if self.yunits.get() == True:
            self.data.ytitle = self.ent_ytitle.get() + " (V)"
        
        self.data.updateplot()
        if (unit.isalpha() == False):
            unit=''
        if self.data.tcursor_delta != 0.0:
            self.tcursor_info.set(f"T1 = {round(self.data.tcursor1_t,7)} {unit}s\nT2 = {round(self.data.tcursor2_t,7)} {unit}s\n" + 
                                f"ΔT = {round(self.data.tcursor_delta,7)} {unit}s\n" +
                                f"1/ΔT = {abs(round(1 / self.data.tcursor_delta, 7))} {funit}Hz")
        else:
            self.tcursor_info.set(f"T1 = {round(self.data.tcursor1_t,7)} {unit}s\nT2 = {round(self.data.tcursor2_t,7)} {unit}s\n" + 
                                f"ΔT = {round(self.data.tcursor_delta,7)} {unit}s\n" +
                                f"1/ΔT = ∞ {funit}Hz")

        for i in range(self.data.n_channels):
            self.chan_cursorinfo[i].set(f"V1 = {round(self.data.cursor1_v[i] * float(self.chan_vdiv[i].get()), 5)} V\nV2 = {round(self.data.cursor2_v[i] * float(self.chan_vdiv[i].get()), 5)} V\n" +
                                        f"ΔV = {round(self.data.cursor_delta[i] * float(self.chan_vdiv[i].get()), 5)} V")

# Start the application
if __name__ == "__main__":
    window = tk.Tk()
    app = TC1ScopeApp(window)
    window.mainloop()
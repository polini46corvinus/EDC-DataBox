# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 19:40:04 2026
@author: 404 csapat (https://github.com/polini46corvinus/EDC-DataBox)
"""

#--------------# Prerequisites
# Python         3.14.2 (or higher)
# Numpy          2.4.0 (or higher)
# Pandas         2.3.3 (or higher)
# Customtkinter  5.2.2 (or higher)
# Pillow         12.1.1 (or higher)

#--------------# Libraries
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from threading import Thread


#--------------# Globals
windowGeometry="800x600+1000+200"
windowTitle="EDC DataBox v0.1"
data1=[]
data2=[]
data3=[]
dataoutput=[]

#--------------# Globals
#color codes: #EBEBEB #0A2239 #3B8ED0 #BFBFBF

#--------------# Initialization
try: 
    import numpy as np
    import pandas as pd
    import customtkinter as ctk
    from PIL import Image
except Exception as ex:
    import subprocess
    if ("No module named 'numpy'" in str(ex)) or ("No module named 'pandas'" in str(ex)) or ("No module named 'customtkinter'" in str(ex) or ("No module named 'PIL'" in str(ex))):
        if mb.askyesno(windowTitle,f"Hiba:\n{ex}\n\nLehet, hogy nincs telepítve valamelyik bővítőcsomag.\nSzeretnéd egyszerre mindegyiket telepíteni?"):
            subprocess.call('start cmd /k "pip install numpy & pip install pandas & pip install customtkinter & pip install pillow & echo. & echo A telepítés befejeződött & echo Zárd be ezt az ablakot, majd futtasd újra az EDC DataBox-ot!"', shell=True)
    else:
        mb.showerror(windowTitle,f"Hiba történt valamely bővítőcsomag betöltésekor:\n{ex}\nKérlek, telepítsd manuálisan!")
    exit()

#--------------# Functions
def open_file_dialog(label):
    label.delete(0,tk.END)
    label.insert(0,fd.askopenfilename(filetypes=[("Excel vagy CSV (.xlsx .xls .csv)", ".xlsx .xls .csv")]))
    return

def helpFile():
    try:
        import subprocess
        subprocess.call('start cmd /c lib\\dokumentacio.pdf', shell=True)
    except Exception as ex:
        mb.showwarning(windowTitle,f"Dokumentáció nem található!\n{ex}")
    return

def startProcess():
    try:
        button_startButton.configure(state="disabled")
        button_stopButton.configure(state="normal")
        progressBar.configure(progress_color="#3B8ED0")
        progressBar.start()
        readFiles()
    except Exception as ex:
        mb.showerror(windowTitle,f"Hiba:\n{ex}\n")
        stopProcess()
    return

def stopProcess():
    try:
        button_startButton.configure(state="normal")
        button_stopButton.configure(state="disabled")
        progressBar.configure(progress_color="#C9C9C9")
        progressBar.stop()
    except Exception as ex:
        mb.showerror(windowTitle,f"Hiba:\n{ex}\n")
    return

def readFiles():
    global data1
    data1 = pd.read_excel(entry_pathFile1.get()) # ide kéne még valami encoding utf8 just in case
    return

#--------------# UI items
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title(windowTitle)
root.geometry(windowGeometry)
root.resizable(False, False)
root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

blueFrame = ctk.CTkFrame(master=root, width=60, height=2000, fg_color="#0A2239", corner_radius=0)
blueFrame.place(x=0, y=0)

label_edcLogo = ctk.CTkLabel(root, text="EDC DataBox", font=ctk.CTkFont(family="Arial Bold", size=26, weight="bold"))
label_edcLogo.place(x=100, y=35)

try:
    image_logo_label = ctk.CTkLabel(root, image=ctk.CTkImage(light_image=Image.open("./lib/logo"), size=(179,30)), text="")
    image_logo_label.place(relx=0.97, rely=0.03, anchor="ne")
except Exception as ex:
    mb.showerror(windowTitle,f"Hiba:\n{ex}\n")
    pass

greyFrame = ctk.CTkFrame(master=root, width=200, height=5, corner_radius=2, fg_color="#3B8ED0")
greyFrame.place(x=100, y=70)

label_loadFile1 = ctk.CTkLabel(root, text="Első fájl útvonala:")
label_loadFile1.place(x=100, y=110)
label_loadFile2 = ctk.CTkLabel(root, text="Második fájl útvonala:")
label_loadFile2.place(x=100, y=140)

entryPlaceholderText="pl. C:/adatok.xlsx, vagy kattints a Megnyitás gombra"
entry_pathFile1 = ctk.CTkEntry(root, width=400, placeholder_text=entryPlaceholderText)
entry_pathFile1.place(x=230, y=110)
entry_pathFile2 = ctk.CTkEntry(root, width=400, placeholder_text=entryPlaceholderText)
entry_pathFile2.place(x=230, y=140)

button_loadFile1 = ctk.CTkButton(root, text="Megnyitás", command=lambda: open_file_dialog(entry_pathFile1))
button_loadFile1.place(relx=0.97, anchor="e", y=124)
button_loadFile2 = ctk.CTkButton(root, text="Megnyitás", command=lambda: open_file_dialog(entry_pathFile2))
button_loadFile2.place(relx=0.97, anchor="e", y=154)

radio_var = tk.IntVar(value=1)
radioButton_1 = ctk.CTkRadioButton(root, text="Egy adatfájl előkészítése", variable=radio_var, value=1)
radioButton_1.place(x=100, y=200)
radioButton_2 = ctk.CTkRadioButton(root, text="Két adatfájl előkészítése és egyesítése", variable=radio_var, value=2)
radioButton_2.place(x=100, y=230)

progressBar = ctk.CTkProgressBar(root, width=200, height=5, corner_radius=2, fg_color="#C9C9C9", progress_color="#C9C9C9", mode="indeterminate")
progressBar.set(0)
progressBar.place(x=100, y=290)

button_startButton = ctk.CTkButton(root, text="Indítás", state="normal", command=lambda: startProcess())
button_startButton.place(x=100, y=310)
button_stopButton = ctk.CTkButton(root, text="Megállítás", state="disabled", command=lambda: stopProcess())
button_stopButton.place(x=100, y=340)

button_helpButton = ctk.CTkButton(root, width=70, text="Segítség", command=helpFile)
button_helpButton.place(relx=0.97, rely=0.97, anchor="se")

root.mainloop()
exit()
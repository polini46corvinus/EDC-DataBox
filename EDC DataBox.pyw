# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 19:40:04 2026
@author: 404 csapat (https://github.com/polini46corvinus/EDC-DataBox)
"""

#--------------# Prerequisites
# Python   3.14.2 (or higher)
# Pandas   2.3.3 (or higher)
# Numpy    2.4.0 (or higher)

#--------------# Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from threading import Thread

#--------------# Globals
windowGeometry="500x500+1200+500"
windowTitle="EDC DataBox"

#--------------# Initialization
try: 
    import numpy as np
    import pandas as pd
    import customtkinter as ctk
except Exception as ex:
    import subprocess
    if ("No module named 'numpy'" in str(ex)) or ("No module named 'pandas'" in str(ex)) or ("No module named 'customtkinter'" in str(ex)):
        if mb.askyesno(windowTitle,f"Hiba:\n{ex}\n\nLehet, hogy nincs telepítve valamelyik bővítőcsomag.\nSzeretnéd egyszerre mindegyiket telepíteni?"):
            subprocess.call('start cmd /k "pip install numpy & pip install pandas & pip install customtkinter & echo. & echo A telepítés befejeződött & echo Zárd be ezt az ablakot, majd futtasd újra az EDC DataBox-ot!"', shell=True)
    else:
        mb.showerror(windowTitle,f"Hiba történt valamely bővítőcsomag betöltésekor:\n{ex}\nKérlek, telepítsd manuálisan!")
    exit()

#--------------# Functions



#--------------# UI items
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title(windowTitle)
root.geometry(windowGeometry)
root.resizable(False, False)

def button_function():
    print("button pressed")

# Use CTkButton instead of tkinter Button
button = ctk.CTkButton(root, text="CTkButton", command=button_function)
button.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()
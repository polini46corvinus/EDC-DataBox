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
except Exception as ex:
    import subprocess
    if ("No module named 'numpy'" in str(ex)) or ("No module named 'pandas'" in str(ex)):
        if "No module named 'numpy'" in str(ex):
            if mb.askyesno(windowTitle,f"Hiba:\n{ex}\n\nLehet, hogy nincs telepítve a numpy.\nSzeretnéd most telepíteni?"):
                subprocess.call('start cmd /k "pip install numpy & echo. & echo A telepítés befejeződött & echo Zárd be ezt az ablakot, majd futtasd újra az EDC DataBox-ot!"', shell=True)
        if "No module named 'pandas'" in str(ex):
            if mb.askyesno(windowTitle,f"Hiba:\n{ex}\n\nLehet, hogy nincs telepítve a pandas.\nSzeretnéd most telepíteni?"):
                subprocess.call('start cmd /k "pip install pandas & echo. & echo A telepítés befejeződött & echo Zárd be ezt az ablakot, majd futtasd újra az EDC DataBox-ot!"', shell=True)
    else:
        mb.showerror(windowTitle,f"Hiba történt valamely bővítőcsomag betöltésekor:\n{ex}")
    exit()


#--------------# Functions

 

#--------------# UI items
root = tk.Tk()
root.title(windowTitle)
root.geometry(windowGeometry)
root.resizable(False, False)


root.mainloop()
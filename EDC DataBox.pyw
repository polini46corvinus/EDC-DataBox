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
# Openpyxl       3.1.5 (or higher)


#--------------# Libraries
import os
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from threading import Thread
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(BASE_DIR, "lib")

#--------------# Globals
windowGeometry="800x600+1000+200"
windowTitle="EDC DataBox v0.3"
data1=[] # branches_2025_anonym.xlsx
data2=[] # branches_anonym.xlsx
data3=[] # companies_anonym.xlsx
datamerge=[]
locations=[] # to be populated by function getLocations
#color codes: #EBEBEB #1D283E #1F538D #BFBFBF #E7E7E7


#--------------# Initialization
try: 
    import numpy as np
    import pandas as pd
    import openpyxl #in case pandas cannot read csvs
    import customtkinter as ctk
    from PIL import Image
except Exception as ex:
    import subprocess
    if ("No module named 'numpy'" in str(ex))  or ("No module named 'pandas'" in str(ex)) or ("No module named 'customtkinter'" in str(ex) or ("No module named 'PIL'" in str(ex)) or ("No module named 'openpyxl'" in str(ex))):
        if mb.askyesno(windowTitle,f"Hiba:\n{ex}\n\nLehet, hogy nincs telepítve valamelyik bővítőcsomag.\nSzeretnéd egyszerre mindegyiket telepíteni?"):
            subprocess.call('start cmd /k "pip install numpy & pip install pandas & pip install customtkinter & pip install pillow & pip install openpyxl & echo. & echo A telepítés befejeződött & echo Zárd be ezt az ablakot, majd futtasd újra az EDC DataBox-ot!"', shell=True)
    else:
        mb.showerror(windowTitle,f"Hiba történt valamely bővítőcsomag betöltésekor:\n{ex}\nKérlek, telepítsd manuálisan!")
    exit()

# %%
#--------------# Functions
def cleanDf(df, mode):
    startProgress("Folyamatban: Adatbázisok előkészítése")
    if "Unnamed: 0" in df.columns: #drop unnamed index column from csvs
        df = df.drop("Unnamed: 0", axis=1)
    if mode=="branches": #else: keep all columns
        df = df.iloc[:,0:9] #enough to keep first 9 cols, last col should be "Házszám"
    if mode=="companies":
        df = df.iloc[:,0:12] #enough to keep first 12 cols, last col should be "Utolsó mérleg dátuma"
        df["'Alapítás éve'"] = df["'Alapítás éve'"].fillna(0).astype(int) #fix for issue: missing values caused the whole column to be filled with nan
    renameCols(df) #removes apostrophe from column names starts and ends
    stripChar_From_StringCols(df, "'") #removes apostrophe from string values starts and ends
    replaceWhiteSpaces_In_StringCols(df)
    stopProgress()
    return df

def renameCols(df): #removes apostrophe from column name starts and ends
    col_names_cleaned = [x.strip("'") for x in df.columns]
    df.columns = col_names_cleaned
    return df

def stripChar_From_StringCols(df, char):
    stringCols = (df.dtypes=="str") | (df.dtypes=="object")
    for i in df.columns[stringCols]:
        df[i] = df[i].str.strip(char)
    return df

def replaceWhiteSpaces_In_StringCols(df):
    stringCols = (df.dtypes=="str") | (df.dtypes=="object")
    for i in df.columns[stringCols]:
        df[i] = df[i].str.replace(r"\s+", " ", regex=True)
    return df

def getLocations():
    global locations
    startProgress("Folyamatban: Irányítószám adatbázis betöltése")

    try: #read zipcode xlsx files
        hnt = pd.read_excel(os.path.join(LIB_DIR, "hnt_letoltes_2025.xlsx"), sheet_name=1, skiprows=2)
        hnt_extras = pd.read_excel(os.path.join(LIB_DIR, "hnt_letoltes_2025.xlsx"), sheet_name=0, skiprows=2)
        with pd.ExcelFile(os.path.join(LIB_DIR, "Iranyitoszam-Internet_uj.xlsx")) as xls:
            posta = pd.read_excel(xls, sheet_name=0, skiprows=1)
            bp = pd.read_excel(xls, sheet_name=2)
            miskolc = pd.read_excel(xls, sheet_name=3)
            debrecen = pd.read_excel(xls, sheet_name=4)
            szeged = pd.read_excel(xls, sheet_name=5)
            pecs = pd.read_excel(xls, sheet_name=6)
            gyor = pd.read_excel(xls, sheet_name=7)
    except Exception as ex:
        mb.showerror("hiba",f"Hiba:\n{ex}\n")
        exit()
    
    hnt = hnt.iloc[:,[1,5]].drop_duplicates() #selects name and all corresponding zipcodes
    hnt.columns=["Település","Irsz"]
    hnt_extras = hnt_extras.iloc[:,[0,2,3,5]] #selects extra cols for later use
    hnt_extras = hnt_extras[hnt_extras.iloc[:,0]!="Összesen"] #deletes last row "Összesen"
    hnt_extras.columns = ["Település", "Jogállás", "Vármegye", "Járás"]
    posta = posta.iloc[:,[0,1]].drop_duplicates()
    posta.columns=["Irsz","Település"]
    bp_dict = {"0": "Budapest Margit-Sziget", "Margitsziget": "Budapest Margit-Sziget",
        "I.": "Budapest 01. kerület", "II.": "Budapest 02. kerület", "III.": "Budapest 03. kerület",
        "IV.": "Budapest 04. kerület", "V.": "Budapest 05. kerület", "VI.": "Budapest 06. kerület",
        "VII.": "Budapest 07. kerület", "VIII.": "Budapest 08. kerület", "IX.": "Budapest 09. kerület",
        "X.": "Budapest 10. kerület", "XI.": "Budapest 11. kerület", "XII.": "Budapest 12. kerület",
        "XIII.": "Budapest 13. kerület", "XIV.": "Budapest 14. kerület", "XV.": "Budapest 15. kerület",
        "XVI.": "Budapest 16. kerület", "XVII.": "Budapest 17. kerület", "XVIII.": "Budapest 18. kerület",
        "XIX.": "Budapest 19. kerület", "XX.": "Budapest 20. kerület", "XXI.": "Budapest 21. kerület",
        "XXII.": "Budapest 22. kerület", "XXIII.": "Budapest 23. kerület"}
    szotar = pd.DataFrame(bp_dict.items(), columns=["KER","new"])
    stripChar_From_StringCols(bp, " ")
    stripChar_From_StringCols(hnt_extras, " ") #just in case
    bp = pd.merge(bp.iloc[:,[0,-1]], szotar, how="left", on="KER").drop_duplicates()
    bp = bp.drop("KER", axis=1)
    bp.columns=["Irsz","Település"]
    
    def cleanCities(df, city): #keeps zip and city names only
        df = pd.DataFrame(df.iloc[:,0]).drop_duplicates()
        df["Település"] = city
        df.columns=["Irsz","Település"]
        return df
    
    miskolc = cleanCities(miskolc, "Miskolc")
    debrecen = cleanCities(debrecen, "Debrecen")
    szeged = cleanCities(szeged, "Szeged")
    pecs = cleanCities(pecs, "Pécs")
    gyor = cleanCities(gyor, "Győr")
    
    locations = pd.concat(objs=[hnt, posta, bp, miskolc, debrecen, szeged, pecs, gyor])
    locations = locations[locations["Irsz"]!="*"] #removes Budapest districts without zipcode distinction
    locations = locations[~((locations["Település"]=="Budapest") & (locations["Irsz"]==1007))] #removes one known bad value which already exists as "Budapest Margit-Sziget"
    locations["Település"] = locations["Település"].str.strip() #cleans all whitespaces, mostly from "posta" database
    locations["Irsz"] = locations["Irsz"].astype(str)
    locations["Irsz"] = locations["Irsz"].str.split("/").str[0] #removes bad value: "1172/1173"
    locations["Irsz"] = locations["Irsz"].astype(int)
    locations = locations[(locations["Irsz"] > 999) & (locations["Irsz"] < 10001)] #extra safety filter for bad values
    locations["Irsz"] = locations["Irsz"].astype(str)
    locations = pd.merge(locations, hnt_extras, on="Település", how="left") #adds extra information to all settlements
    mask = locations["Település"].str.startswith("Budapest")
    locations.loc[mask, ["Jogállás", "Vármegye", "Járás"]] = ["főváros", "Budapest", "Budapesti"]
    locations = locations.drop_duplicates().sort_values(by="Irsz").reset_index(drop=True)
    locations = locations.dropna() #removes one NaN value which was created by Irsz 1007 (Margit-Sziget)
    del mask
    
    #v0.3 (2026.05.15.):
    #Quick & dirty method to avoid data duplication during merging due to multiple settlement/zipcode pairs exist.
    #Using the method of selecting the first element, we choose to keep the largest, then order by name
    #Keep first settlement method:
        #Creates a list of settlement labels, ordered by size ascending
        #Creates a new col in locations and assigns an integer to each based on settlement size
    settlementDict = {"község":0, "nagyközség":1, "város":2, "megyei jogú város":3, "megyeszékhely, megyei jogú város":4, "főváros":5}
    locations["settlementSizeOrder"] = locations["Jogállás"].map(settlementDict)
    locations = locations.sort_values(by=["Irsz", "settlementSizeOrder", "Település"], ascending=[True, False, True])
    locations = locations.drop_duplicates(subset=["Irsz"],keep="first")
    locations = locations.drop("settlementSizeOrder", axis="columns") #unnecessary from now on

    stopProgress()
    return locations

def open_file_dialog(label):
    label.delete(0,tk.END)
    label.insert(0,fd.askopenfilename(filetypes=[("Excel vagy CSV (.xlsx .xls .csv)", ".xlsx .xls .csv")]))
    return

def helpFile():
    try:
        import subprocess
        subprocess.call(f'start cmd /c "{os.path.join(LIB_DIR, "dokumentacio.pdf")}"', shell=True)
    except Exception as ex:
        mb.showwarning(windowTitle,f"Dokumentáció nem található!\n{ex}")
    return

def startProgress(statusLabelText):
    try:
        statusLabel.configure(text=statusLabelText)
        progressBar.configure(progress_color="#1F538D")
        progressBar.start()
        for i in [checkbox, button_startButton, button_loadFile1, button_loadFile2, button_loadFile3]:
            i.configure(state="disabled")

    except Exception as ex:
        mb.showerror(windowTitle,f"Hiba:\n{ex}\n")
        stopProgress()
    return

def stopProgress():
    try:
        statusLabel.configure(text="Kész!")
        progressBar.configure(progress_color="#C9C9C9")
        progressBar.stop()
        for i in [checkbox, button_startButton, button_loadFile1, button_loadFile3]:
            i.configure(state="normal")
        if checkbox.get() == "on":
            button_loadFile2.configure(state="normal")
            
    except Exception as ex:
        mb.showerror(windowTitle,f"Hiba:\n{ex}\n")
    return

def formatBranchesDataCols(data):
    startProgress("Folyamatban: Branches fájl formázása")
    data = data[data["Ország kód"]=="HU"].drop(["Cím típus kód", "Ország kód", "Ország"], axis="columns") #selects only hungarian entities and drops useless cols
    stopProgress()
    return data

def formatCompaniesDataCols(data):
    startProgress("Folyamatban: Companies formázása")
    data = data.drop(["TEÁOR megnevezés", "Járás", "Utolsó mérleg dátuma", "Megye"], axis="columns")
    data = data[data["Jogi státusz"]=="aktív"] #filter only active companies
    stopProgress()
    return data

def readFiles():
    startProgress("Folyamatban: Fájlok beolvasása")
    global data1
    global data2
    global data3
    try:
        if entry_pathFile1.get() != "":
            if "xls" in entry_pathFile1.get().split(".")[1]:
                data1 = pd.read_excel(entry_pathFile1.get())
            if "csv" in entry_pathFile1.get().split(".")[1]:
                data1 = pd.read_csv(entry_pathFile1.get())
        
        if checkbox.get() == "on" and entry_pathFile2.get() != "":
            if "xls" in entry_pathFile2.get().split(".")[1]:
                data2 = pd.read_excel(entry_pathFile2.get())
            if "csv" in entry_pathFile2.get().split(".")[1]:
                data2 = pd.read_csv(entry_pathFile2.get())
        
        if entry_pathFile3.get() != "":
            if "xls" in entry_pathFile3.get().split(".")[1]:
                data3 = pd.read_excel(entry_pathFile3.get())
            if "csv" in entry_pathFile3.get().split(".")[1]:
                data3 = pd.read_csv(entry_pathFile3.get())

    except Exception as ex:
        mb.showerror(windowTitle,f"Hiba: A beolvasandó fájlok útvonalai hibásak!\n{ex}\n")
    
    try:
        if len(data1)>0:
            data1 = cleanDf(data1, "branches")
            data1 = formatBranchesDataCols(data1)
        if len(data2)>0:
            data2 = cleanDf(data2, "branches")
            data2 = formatBranchesDataCols(data2)
        if len(data3)>0:
            data3 = cleanDf(data3, "companies")
            data3 = formatCompaniesDataCols(data3)
            button_saveButton.configure(state="normal")
    except Exception as ex:
        mb.showerror(windowTitle,f"Hiba:\n{ex}\n")
   
    stopProgress()
    return

def checkboxEvent():
    if checkbox.get() == "off":
        entry_pathFile2.delete(0,tk.END)
        entry_pathFile2.configure(placeholder_text="") #has to set placeholder first
        entry_pathFile2.configure(state="disabled") #then disable separately
        button_loadFile2.configure(state="disabled")
        label_loadFile2.configure(text_color="#BDBDBD")
    if checkbox.get() == "on":
        mb.showinfo(windowTitle, "Használat:\n\nElső fájl: idő szerint újabb\nMásodik fájl: idő szerint régebbi")
        entry_pathFile2.configure(state="normal", placeholder_text=entryPlaceholderText)
        button_loadFile2.configure(state="normal")
        label_loadFile2.configure(text_color="#000000")
    return

def saveFile():
    savePath = os.path.join(BASE_DIR,'output.csv')
    if mb.showinfo(windowTitle, f"Az output.csv fájl a feldolgozást követően a program gyökérkönyvtárában megtalálható:\n{savePath}")=="ok":
        try:
            button_saveButton.configure(state="disabled")
            startProgress("Folyamatban: Fájl (output.csv) mentése")
            global data1
            global data2
            global data3
            global datamerge
            #deb = pd.Series(pd.read_excel("debreceni crefok.xlsx").iloc[:,0])
            #data1 = data1.loc[data1["Crefo szám"].isin(deb)]
            #data2 = data2.loc[data2["Crefo szám"].isin(deb)]
            if (len(data1)>0 and len(data2)>0):
                dataconcat = pd.concat([data1, data2])
                del data1, data2
            elif len(data1)>0:
                dataconcat = data1
                del data1
            elif len(data2)>0:
                dataconcat = data2
                del data2
            
            datamerge = pd.merge(dataconcat, data3, how="left", on="Crefo szám")
            del dataconcat, data3
            
            datamerge["Alapítás éve"] = datamerge["Alapítás éve"].fillna(0).astype(int) #lots of empty values were created due to merge
            datamerge = datamerge.drop(["Irányítószám_y", "Település_y", "Cím"], axis="columns") #deleting headquarters addresses
            datamerge = datamerge.replace(["NULL", np.nan],"")
            datamerge = datamerge.rename(columns={"Irányítószám_x":"Irsz", "Település_x": "Település"})
            datamerge = datamerge[datamerge["Irsz"]!=""]
            datamerge["Irsz"] = datamerge["Irsz"].astype(str)
            datamerge = pd.merge(datamerge, locations, on="Irsz", how="left")
            #datamerge = datamerge.drop("Település_y", axis="columns")
            datamerge = datamerge.drop("Település_x", axis="columns") #instead of using original settlement names, use ones derived from locations variable
            #datamerge = datamerge.rename(columns={"Település_x": "Település"})
            datamerge = datamerge.rename(columns={"Település_y": "Település"})
            datamerge["Cím"] = datamerge["Irsz"].str.cat([datamerge["Település"], datamerge["Utca"], datamerge["Házszám"]], sep=", ").str.rstrip(", ")
            datamerge = stripChar_From_StringCols(datamerge, " ")
            datamerge = replaceWhiteSpaces_In_StringCols(datamerge)
            datamerge = datamerge.drop(["Irsz", "Utca", "Házszám"], axis="columns")
            datamerge["Jogi forma"] = datamerge["Jogi forma"].replace("korlátolt felelősségű társaság (Kft.)", "Kft.")
            datamerge["Jogi forma"] = datamerge["Jogi forma"].replace("Betéti társaság (Bt.)", "Bt.")
            
            #--------------# Custom filters
            datamerge = datamerge.replace(["Ô", "ô", "Õ", "õ"], "ő")
            
            
            #--------------# Save
            datamerge = datamerge.drop_duplicates()
            #datamerge.to_excel("debreceni szekhelyu cegek.xlsx", index=False)
            datamerge.to_csv(savePath)
            stopProgress()    
        except Exception as ex:
            mb.showerror(windowTitle,f"Hiba:\n{ex}\n")
        return datamerge
    else:
        return


# %%
#--------------# UI items
ctk.set_appearance_mode("light")
try:
    ctk.set_default_color_theme(os.path.join(LIB_DIR, "dark-blue.json"))
except Exception as ex:
    mb.showerror(windowTitle,f"Hiba:\n{ex}\n")
    pass
root = ctk.CTk()
root.title(windowTitle)
root.geometry(windowGeometry)
root.resizable(False, False)
root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

blueSideFrame = ctk.CTkFrame(master=root, width=60, height=2000, fg_color="#1D283E", corner_radius=0)
blueSideFrame.place(x=0, y=0)

label_edcLogo = ctk.CTkLabel(root, text="EDC DataBox", font=ctk.CTkFont(family="Arial Bold", size=26, weight="bold"))
label_edcLogo.place(x=100, y=35)

try: #logo placement
    image_logo_label = ctk.CTkLabel(root, image=ctk.CTkImage(light_image=Image.open(os.path.join(LIB_DIR, "logo")), size=(179,30)), text="")
    image_logo_label.place(relx=0.97, rely=0.03, anchor="ne")
except Exception as ex:
    mb.showerror(windowTitle,f"Hiba:\n{ex}\n")
    pass

blueLineFrame = ctk.CTkFrame(root, width=200, height=5, corner_radius=2, fg_color="#1F538D")
blueLineFrame.place(x=100, y=70)

darkFrame1 = ctk.CTkFrame(root, width=690, height=150, fg_color="#E7E7E7", corner_radius=10)
darkFrame1.place(x=93, y=105)
label_branchesFiles = ctk.CTkLabel(root, text="Branches fájl(ok):", bg_color="#E7E7E7")
label_branchesFiles.configure(font=("arial",13,"bold"))
label_branchesFiles.place(x=100, y=110)
label_loadFile1 = ctk.CTkLabel(root, text="Első fájl útvonala:", bg_color="#E7E7E7")
label_loadFile1.place(x=100, y=140)
label_loadFile2 = ctk.CTkLabel(root, text="Második fájl útvonala:", bg_color="#E7E7E7", text_color="#BDBDBD")
label_loadFile2.place(x=100, y=170)
check_var = ctk.StringVar(value="off")
checkbox = ctk.CTkCheckBox(root, text="Két Branches fájl előkészítése és egyesítése", border_width=2, command=checkboxEvent, variable=check_var, onvalue="on", offvalue="off", state="disabled", bg_color="#E7E7E7")
checkbox.place(x=100, y=215)
entryPlaceholderText="pl. C:/adatok.xlsx, vagy kattints a Megnyitás gombra"
entry_pathFile1 = ctk.CTkEntry(root, width=385, placeholder_text=entryPlaceholderText, bg_color="#E7E7E7")
entry_pathFile1.place(x=245, y=140)
entry_pathFile2 = ctk.CTkEntry(root, width=385, placeholder_text=entryPlaceholderText, bg_color="#E7E7E7", state="disabled")
entry_pathFile2.place(x=245, y=170)
button_loadFile1 = ctk.CTkButton(root, text="Megnyitás", state="disabled", command=lambda: open_file_dialog(entry_pathFile1))
button_loadFile1.place(relx=0.97, anchor="e", y=154)
button_loadFile2 = ctk.CTkButton(root, text="Megnyitás", state="disabled", command=lambda: open_file_dialog(entry_pathFile2))
button_loadFile2.place(relx=0.97, anchor="e", y=184)

darkFrame2 = ctk.CTkFrame(root, width=690, height=80, fg_color="#E7E7E7", corner_radius=10)
darkFrame2.place(x=93, y=275)
label_companiesFile = ctk.CTkLabel(root, text="Companies fájl:", bg_color="#E7E7E7")
label_companiesFile.configure(font=("arial",13,"bold"))
label_companiesFile.place(x=100, y=280)
label_loadFile3 = ctk.CTkLabel(root, text="Companies fájl útvonala:", bg_color="#E7E7E7")
label_loadFile3.place(x=100, y=310)
entry_pathFile3 = ctk.CTkEntry(root, width=385, placeholder_text=entryPlaceholderText, bg_color="#E7E7E7")
entry_pathFile3.place(x=245, y=310)
button_loadFile3 = ctk.CTkButton(root, text="Megnyitás", state="disabled", command=lambda: open_file_dialog(entry_pathFile3))
button_loadFile3.place(relx=0.97, anchor="e", y=324)


progressBar = ctk.CTkProgressBar(root, width=200, height=5, corner_radius=2, fg_color="#C9C9C9", progress_color="#C9C9C9", mode="indeterminate")
progressBar.set(0)
progressBar.place(x=100, y=380)
statusLabel = ctk.CTkLabel(root, text="")
statusLabel.place(x=310, y=367)
button_startButton = ctk.CTkButton(root, text="Indítás", state="disabled", command=lambda: Thread(target=readFiles).start())
button_startButton.place(x=100, y=400)
button_helpButton = ctk.CTkButton(root, width=70, text="Segítség", command=helpFile)
button_helpButton.place(relx=0.97, rely=0.97, anchor="se")

button_saveButton = ctk.CTkButton(root, text="Mentés", state="disabled", command=lambda: Thread(target=saveFile).start())
button_saveButton.place(x=100, y=430)

# %%

root.after(300, lambda: Thread(target=getLocations).start())
root.mainloop()

exit()

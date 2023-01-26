import pickle
import os,fnmatch
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import re
from tkinter import *
from tkinter import ttk


ABSPATH=os.path.dirname(os.path.abspath(__file__))

def isWindows():
    return os.name=="nt"

if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix

if(isWindows()): 
    PATHLOGBMONFOLDER= ABSPATH+"\\output\\mensile\\logbook\\" #path per windows
else: PATHLOGBMONFOLDER= ABSPATH+"/output/mensile/logbook/" #path per unix

if(isWindows()): 
    PATHGUADMONFOLDER= ABSPATH+"\\output\\mensile\\guadagni\\" #path per windows
else: PATHGUADMONFOLDER= ABSPATH+"/output/mensile/guadagni/" #path per unix

if(isWindows()): 
    PATHLOGBTRIFOLDER= ABSPATH+"\\output\\trimestrale\\logbook\\" #path per windows
else: PATHLOGBTRIFOLDER= ABSPATH+"/output/trimestrale/logbook/" #path per unix

if(isWindows()): 
    PATHGUADTRIFOLDER= ABSPATH+"\\output\\trimestrale\\guadagni\\" #path per windows
else: PATHGUADTRIFOLDER= ABSPATH+"/output/trimestrale/guadagni/" #path per unix

  
def genstockdf():
    stockdf=[]
    stocknames=[] 
    pattern="*.csv"
    i=0
    for stock in os.listdir(PATHCSVFOLDER):
        if(stock!='.DS_Store' and fnmatch.fnmatch(stock, pattern)):
            stocknames.append(stock[:-4])
            path=os.path.join(PATHCSVFOLDER, stocknames[i]+'.csv')
            df=pd.read_csv(path,usecols=["Date","Open","High","Low","Close","Adj Close","Volume"])
            stockdf.append(df)
            i+=1
    return (stockdf,stocknames)

def gendumpnames(path):

    def lensort(filename):
        return len(filename[:filename.find("_MU")])

    dumpnames=[]
    pattern="*.dump"
    i=0

    for dump in os.listdir(path):
        if(dump!='.DS_Store' and fnmatch.fnmatch(dump, pattern)):
            dumpnames.append(dump[:-5])
            i+=1

    dumpnames.sort(key=lensort)
    return dumpnames

def gendumpnamesReg(path):

    def grp(pat, txt): 
        r = re.search(pat, txt)
        return r.group(0) if r else '&'

    dumpnames=[]
    pattern="*.dump"
    i=0

    for dump in os.listdir(path):
        if(dump!='.DS_Store' and fnmatch.fnmatch(dump, pattern)):
            dumpnames.append(dump[:-5])
            i+=1
    dumpnames.sort(key=lambda l: grp(r'\d+', l))
    # dumpnames.sort(key=lensort)
    return dumpnames

def genportfolio(ind):
    listportfoliotitle=[]
    for i,stock in enumerate(stocknames):
        if(ind[i]!=0):
            listportfoliotitle.append(f'{stock}:{int(ind[i])}')
            # listportfoliotitle.append([stock,int(ind[i])])
    return listportfoliotitle

def tkChooseButton():
    win = Tk()
    win.title("PlotLoader")
    win.geometry("250x125")

    def sceltamensile():
        global scelta
        scelta=1
        win.destroy()

    def sceltatrimestrale():
        global scelta
        scelta=2
        win.destroy()

    Label(win, text="Seleziona file da visualizzare").pack()
    Button(win, text='MENSILI', command=sceltamensile,bg='#3A75C4',fg='black',width=30,pady=10).pack()
    Button(win, text='TRIMESTRALI', command=sceltatrimestrale,bg='#3A75C4',fg='black',width=30,pady=10).pack()
    win.mainloop()   

def tkloadmensile(logbnames,guadagninames):
  
    win = Tk()
    win.title("PlotLoader Mensile")
    win.geometry("620x144")
    win.columnconfigure(0,weight=1)
    win.columnconfigure(1,weight=1)

    def closewin():
        win.destroy()

    def plotmon():
        logbpath=os.path.join(PATHLOGBMONFOLDER, logb.get())+'.dump'
        guadpath=os.path.join(PATHGUADMONFOLDER, guad.get())+'.dump'
        loadmon(logbpath,guadpath)

    Label(win, text="Seleziona file da visualizzare").grid(column=0,row=0,columnspan=2,pady=2)
    
    logb=StringVar()
    logb_combobox = ttk.Combobox(win, textvariable=logb,justify=CENTER)
    logb_combobox.set("Lista Logbook")
    logb_combobox['values']=logbnames
    logb_combobox['state']='readonly'
    logb_combobox.grid(column=0,row=1,columnspan=2,pady=2,padx=5,sticky='nesw')
    # logb_combobox.bind('<<ComboboxSelected>>',selectlogb)
  
    guad=StringVar()
    guad_combobox = ttk.Combobox(win, textvariable=guad,justify=CENTER)
    guad_combobox.set("Lista Guadagni")
    guad_combobox['values']=guadagninames
    guad_combobox['state']='readonly'
    guad_combobox.grid(column=0,row=3,columnspan=2,pady=15,padx=5,sticky='nesw')
    # guad_combobox.bind('<<ComboboxSelected>>',selectguad)

    plotbutton=Button(win, text='PLOT', command=plotmon,bg='#3A75C4',fg='black')
    plotbutton.grid(column=0, row=4,padx=10,sticky='nesw')
    closebutton=Button(win, text='ESCI', command=closewin,bg='#7B1B02',fg='black')
    closebutton.grid(column=1, row=4,padx=10,sticky='nesw')

    win.mainloop()   

def tkloadtrimestrale(logbnames,guadagninames):
  
    win = Tk()
    win.title("PlotLoader Trimestrale")
    win.geometry("620x144")
    win.columnconfigure(0,weight=1)
    win.columnconfigure(1,weight=1)

    def closewin():
        win.destroy()

    def plottrim():
        logbpath=os.path.join(PATHLOGBTRIFOLDER, logb.get())+'.dump'
        guadpath=os.path.join(PATHGUADTRIFOLDER, guad.get())+'.dump'
        loadtrim(logbpath,guadpath)

    Label(win, text="Seleziona file da visualizzare").grid(column=0,row=0,columnspan=2,pady=2)
    
    logb=StringVar()
    logb_combobox = ttk.Combobox(win, textvariable=logb,justify=CENTER)
    logb_combobox.set("Lista Logbook")
    logb_combobox['values']=logbnames
    logb_combobox['state']='readonly'
    logb_combobox.grid(column=0,row=1,columnspan=2,pady=2,padx=5,sticky='nesw')
    # logb_combobox.bind('<<ComboboxSelected>>',selectlogb)
  
    guad=StringVar()
    guad_combobox = ttk.Combobox(win, textvariable=guad,justify=CENTER)
    guad_combobox.set("Lista Guadagni")
    guad_combobox['values']=guadagninames
    guad_combobox['state']='readonly'
    guad_combobox.grid(column=0,row=3,columnspan=2,pady=15,padx=5,sticky='nesw')
    # guad_combobox.bind('<<ComboboxSelected>>',selectguad)

    plotbutton=Button(win, text='PLOT', command=plottrim,bg='#3A75C4',fg='black')
    plotbutton.grid(column=0, row=4,padx=10,sticky='nesw')
    closebutton=Button(win, text='ESCI', command=closewin,bg='#7B1B02',fg='black')
    closebutton.grid(column=1, row=4,padx=10,sticky='nesw')

    win.mainloop()   

def loadmon(logbpath,guadpath):
    logbfile=logbpath[len(PATHLOGBMONFOLDER):-5]
    guadfile=guadpath[len(PATHGUADMONFOLDER):-5]
    logbooks=pickle.load(open(logbpath,"rb"))
    guadagni=pickle.load(open(guadpath,"rb"))
    
    listguadagni=[]
    maxguadagno=0
    for ind in guadagni:
        if ind[1]>=maxguadagno:
            maxguadagno=ind[1]
            bestind=[ind[0],genportfolio(ind[2])]
        listguadagni.append(ind[1])

    listavgrisk=[]
    listavgyield=[]
    for logb in logbooks:
        for stat in logb:
            avgrisk=stat["avg"][0]
            avgyield=stat["avg"][1]
            listavgrisk.append(avgrisk)
            listavgyield.append(avgyield)

    plotall(listguadagni,bestind,listavgrisk,listavgyield,logbfile,guadfile)

def loadtrim(logbpath,guadpath):
    logbfile=logbpath[len(PATHLOGBTRIFOLDER):-5]
    guadfile=guadpath[len(PATHGUADTRIFOLDER):-5]
    logbooks=pickle.load(open(logbpath,"rb"))
    guadagni=pickle.load(open(guadpath,"rb"))
    
    listguadagni=[]
    maxguadagno=0
    for ind in guadagni:
        if ind[1]>=maxguadagno:
            maxguadagno=ind[1]
            bestind=[ind[0],genportfolio(ind[2])]
        listguadagni.append(ind[1])

    listavgrisk=[]
    listavgyield=[]
    for logb in logbooks:
        for stat in logb:
            avgrisk=stat["avg"][0]
            avgyield=stat["avg"][1]
            listavgrisk.append(avgrisk)
            listavgyield.append(avgyield)

    plotall(listguadagni,bestind,listavgrisk,listavgyield,logbfile,guadfile)

def plotall(listguadagni,bestind,listavgrisk,listavgyield,logbfile,guadfile):

    paramRegex=r"^[A-Z\[a-z\]]+[_]?[ ]?[0-9]+|[A-Z\[a-z\]]+[=][0-9\[.\]]+"
    matchlogb= re.findall(paramRegex, logbfile)
    matchguad= re.findall(paramRegex, guadfile)

    idfileRegex= re.compile(r'\d+')
    idlogb= idfileRegex.search(matchlogb[0]).group()
    idguad= idfileRegex.search(matchguad[0]).group()

    
    if (matchlogb[1:]==matchguad[1:]) and (int(idlogb)==int(idguad)):
        
        plt.style.use("ggplot")
        fig = plt.figure(f"GRAFICO DI {str(matchguad[1:])[1:-1]}",figsize=(13,6))

        maxtime=int(str(matchguad[4])[8:])
        datelogb=pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(listavgrisk))
        dateguad=pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(listguadagni))
        bestdate=pd.to_datetime(stockdf[0]["Date"][bestind[0]-1])
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    
        fig.suptitle(f"Miglior Portfolio il {str(bestdate)[:-9]}\n{bestind[1]}")
        
        yplt = plt.subplot2grid((3, 3), loc=(0, 0),colspan=3)
        yplt.plot(datelogb,listavgyield,label=f"Yield avg: {np.mean(listavgyield)}",color="green")
        yplt.set_title(f"Config: {str(matchguad[1:-1])[1:-1]}")
        yplt.legend(frameon=False)

        rplt = plt.subplot2grid((3, 3), loc=(1, 0),colspan=3)
        rplt.plot(datelogb,listavgrisk,label=f"Risk avg: {np.mean(listavgrisk)}",color="red")
        rplt.legend(frameon=False)

        gplt = plt.subplot2grid((3, 3), loc=(2, 0),colspan=3)
        gplt.plot(dateguad,listguadagni,label=f"Valore Portfolio con € {str(idfileRegex.search(matchguad[-1]).group())}",color="blue",marker='o')
        # gplt.plot(dateguad,listguadagni,label=f"Valore Portfolio con {str(matchguad[-1:])[2:-2]}€",color="blue",marker='o')
        gplt.scatter(bestdate,(np.max(listguadagni)),s=125,label=f"Guadagno Miglior Portfolio: {np.max(listguadagni)}")
        gplt.set_xlabel(f'Data\nDal {stockdf[0]["Date"][0]} al {stockdf[0]["Date"][maxtime-1]}') 
        gplt.legend(frameon=False)
        
        # fig.legend(loc="lower left", title="", frameon=False)
        fig.tight_layout(h_pad=-1)
        plt.gcf().autofmt_xdate()
        plt.show()
    else:
        return print("I file non sono compatibili")

def main():
    tkChooseButton()
    if scelta==1:
        tkloadmensile(gendumpnames(PATHLOGBMONFOLDER),gendumpnames(PATHGUADMONFOLDER))
    elif scelta==2:
        tkloadtrimestrale(gendumpnames(PATHLOGBTRIFOLDER),gendumpnames(PATHGUADTRIFOLDER))
    else: print("scelta errata")

if __name__ == "__main__":
    stockdf,stocknames= genstockdf()
    main()
                            





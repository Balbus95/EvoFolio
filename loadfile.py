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

if(isWindows()): #path per windows
    PATHCSVFOLDER=ABSPATH+"\\stock\\WEEK\\" 
    PATHLOGBMONFOLDER=ABSPATH+"\\output\\mensile\\logbook\\"
    PATHGUADMONFOLDER=ABSPATH+"\\output\\mensile\\guadagni\\"
    PATHLOGBTRIFOLDER=ABSPATH+"\\output\\trimestrale\\logbook\\"
    PATHGUADTRIFOLDER=ABSPATH+"\\output\\trimestrale\\guadagni\\"
else: #path per unix
    PATHCSVFOLDER=ABSPATH+"/stock/WEEK/" 
    PATHLOGBMONFOLDER=ABSPATH+"/output/mensile/logbook/"
    PATHGUADMONFOLDER=ABSPATH+"/output/mensile/guadagni/"
    PATHLOGBTRIFOLDER=ABSPATH+"/output/trimestrale/logbook/"
    PATHGUADTRIFOLDER=ABSPATH+"/output/trimestrale/guadagni/"

def genstockdf(pathfolder): # returns a list of dataframe and the list of stock names
    stockdf=[]
    stocknames=[] 
    pattern="*.csv"
    i=0
    for stock in sorted(os.listdir(pathfolder)):
        if(stock!='.DS_Store'and fnmatch.fnmatch(stock, pattern)):
            stocknames.append(stock[:-4])
            path=os.path.join(pathfolder, stocknames[i]+'.csv')
            df=pd.read_csv(path,usecols=["Date","Open","High","Low","Close","Adj Close","Volume"])
            stockdf.append(df)
            i+=1
    return (stockdf,stocknames)

def gendumpnames(path):  # returns a list of dump name 

    def lensort(filename):
        return len(filename[:filename.find("_MU")])

    dumpnames=[]
    pattern="*.dump"

    for dump in sorted(os.listdir(path)):
        if(dump!='.DS_Store' and fnmatch.fnmatch(dump, pattern)):
            dumpnames.append(dump[:-5])

    dumpnames.sort(key=lensort)
    return dumpnames

def gendumpnamesReg(path): # non usato

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
    return dumpnames

def genportfolio(ind): #returns the portfolio of ind with titles
    listportfoliotitle=[]
    for i,stock in enumerate(stocknames):
        if(ind[i]!=0):
            listportfoliotitle.append(f'{stock}:{int(ind[i])}')
            # listportfoliotitle.append([stock,int(ind[i])])
    return listportfoliotitle

def tkChooseButton(): # GUI used to choose which configuration to see
    win = Tk()
    win.title("PlotLoader")
    win.geometry("250x160")

    def sceltamensile():
        global scelta
        scelta=1
        win.destroy()

    def sceltatrimestrale():
        global scelta
        scelta=2
        win.destroy()

    def closewin():
        global scelta
        scelta=0
        win.destroy()

    Label(win, text="Select files to plot").pack()
    Button(win, text='MONTHLY', command=sceltamensile,bg='#3A75C4',fg='black',width=30,pady=10).pack()
    Button(win, text='TRIMESTRAL', command=sceltatrimestrale,bg='#3A75C4',fg='black',width=30,pady=10).pack()
    Button(win, text='EXIT', command=closewin,bg='#7B1B02',fg='black',width=15,pady=10).pack()
    win.mainloop()   

def tkloadmensile(logbnames,guadagninames): # GUI used to choose which monthly configuration to see
  
    win = Tk()
    win.title("PlotLoader Monthly")
    win.geometry("620x144")
    win.columnconfigure(0,weight=1)
    win.columnconfigure(1,weight=1)

    def checklobg(event):
        value = event.widget.get()

        if value == '':
            logb_combobox['values'] = logbnames
        else:
            data = []
            for item in logbnames:
                if value.lower() in item.lower():
                    data.append(item)

            logb_combobox['values'] = data

    def checkguad(event):
        value = event.widget.get()

        if value == '':
            guad_combobox['values'] = guadagninames
        else:
            data = []
            for item in guadagninames:
                if value.lower() in item.lower():
                    data.append(item)

            guad_combobox['values'] = data

    def closewin():
        win.destroy()

    def plotmon():
        logbpath=os.path.join(PATHLOGBMONFOLDER, logb.get())+'.dump'
        guadpath=os.path.join(PATHGUADMONFOLDER, guad.get())+'.dump'
        loadmon(logbpath,guadpath)

    Label(win, text="Select files to plot").grid(column=0,row=0,columnspan=2,pady=2)
    
    logb=StringVar()
    logb_combobox = ttk.Combobox(win, textvariable=logb,justify=CENTER)
    logb_combobox.set("Logb_")
    logb_combobox['values']=logbnames
    logb_combobox.bind('<KeyRelease>',checklobg)
    logb_combobox.grid(column=0,row=1,columnspan=2,pady=2,padx=5,sticky='nesw')

    guad=StringVar()
    guad_combobox = ttk.Combobox(win, textvariable=guad,justify=CENTER)
    guad_combobox.set("Guad_")
    guad_combobox['values']=guadagninames
    guad_combobox.bind('<KeyRelease>',checkguad)
    guad_combobox.grid(column=0,row=3,columnspan=2,pady=15,padx=5,sticky='nesw')

    plotbutton=Button(win, text='PLOT', command=plotmon,bg='#3A75C4',fg='black')
    plotbutton.grid(column=0, row=4,padx=10,sticky='nesw')
    closebutton=Button(win, text='EXIT', command=closewin,bg='#7B1B02',fg='black')
    closebutton.grid(column=1, row=4,padx=10,sticky='nesw')

    win.mainloop()   

def tkloadtrimestrale(logbnames,guadagninames): # GUI used to choose which trimestral configuration to see
  
    win = Tk()
    win.title("PlotLoader Trimestral")
    win.geometry("620x144")
    win.columnconfigure(0,weight=1)
    win.columnconfigure(1,weight=1)

    def checklobg(event):
        value = event.widget.get()

        if value == '':
            logb_combobox['values'] = logbnames
        else:
            data = []
            for item in logbnames:
                if value.lower() in item.lower():
                    data.append(item)

            logb_combobox['values'] = data

    def checkguad(event):
        value = event.widget.get()

        if value == '':
            guad_combobox['values'] = guadagninames
        else:
            data = []
            for item in guadagninames:
                if value.lower() in item.lower():
                    data.append(item)

            guad_combobox['values'] = data

    def closewin():
        win.destroy()

    def plottrim():
        logbpath=os.path.join(PATHLOGBTRIFOLDER, logb.get())+'.dump'
        guadpath=os.path.join(PATHGUADTRIFOLDER, guad.get())+'.dump'
        loadtrim(logbpath,guadpath)

    Label(win, text="Select files to plot").grid(column=0,row=0,columnspan=2,pady=2)
    
    logb=StringVar()
    logb_combobox = ttk.Combobox(win, textvariable=logb,justify=CENTER)
    logb_combobox.set("Logb_")
    logb_combobox['values']=logbnames
    logb_combobox.bind('<KeyRelease>',checklobg)
    logb_combobox.grid(column=0,row=1,columnspan=2,pady=2,padx=5,sticky='nesw')
  
    guad=StringVar()
    guad_combobox = ttk.Combobox(win, textvariable=guad,justify=CENTER)
    guad_combobox.set("Guad_")
    guad_combobox['values']=guadagninames
    guad_combobox.bind('<KeyRelease>',checkguad)
    guad_combobox.grid(column=0,row=3,columnspan=2,pady=15,padx=5,sticky='nesw')

    plotbutton=Button(win, text='PLOT', command=plottrim,bg='#3A75C4',fg='black')
    plotbutton.grid(column=0, row=4,padx=10,sticky='nesw')
    closebutton=Button(win, text='EXIT', command=closewin,bg='#7B1B02',fg='black')
    closebutton.grid(column=1, row=4,padx=10,sticky='nesw')

    win.mainloop()   

def loadmon(logbpath,guadpath): # reads the monthly file and plots it
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

def loadtrim(logbpath,guadpath): # reads the trimestral file and plots it
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

def plotall(listguadagni,bestind,listavgrisk,listavgyield,logbfile,guadfile): #plots two compatible guad and logb files

    paramRegex=r"^[A-Z\[a-z\]]+[_]?[ ]?[0-9]+|[A-Z\[a-z\]]+[=][0-9\[.\]]+"
    matchlogb= re.findall(paramRegex, logbfile)
    matchguad= re.findall(paramRegex, guadfile)

    idfileRegex= re.compile(r'\d+')
    idlogb= idfileRegex.search(matchlogb[0]).group()
    idguad= idfileRegex.search(matchguad[0]).group()

    
    if (matchlogb[1:]==matchguad[1:]) and (int(idlogb)==int(idguad)):
        
        plt.style.use("ggplot")
        fig = plt.figure(f"PLOT OF {str(matchguad[1:])[1:-1]}",figsize=(13,6))

        maxtime=int(str(matchguad[4])[8:])
        datelogb=pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(listavgrisk))
        dateguad=pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(listguadagni))
        bestdate=pd.to_datetime(stockdf[0]["Date"][bestind[0]-1])
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    
        fig.suptitle(f"Best Portfolio {str(bestdate)[:-9]}\n{bestind[1]}")
        
        yplt = plt.subplot2grid((3, 3), loc=(0, 0),colspan=3)
        yplt.plot(datelogb,listavgyield,label=f"Yield avg: {np.mean(listavgyield)}",color="green")
        yplt.set_title(f"Config: {str(matchguad[1:-1])[1:-1]}")
        yplt.legend(frameon=False)

        rplt = plt.subplot2grid((3, 3), loc=(1, 0),colspan=3)
        rplt.plot(datelogb,listavgrisk,label=f"Risk avg: {np.mean(listavgrisk)}",color="red")
        rplt.legend(frameon=False)

        gplt = plt.subplot2grid((3, 3), loc=(2, 0),colspan=3)
        gplt.plot(dateguad,listguadagni,label=f"Portfolio value with € {str(idfileRegex.search(matchguad[-1]).group())}",color="blue",marker='o')
        # gplt.plot(dateguad,listguadagni,label=f"Valore Portfolio con {str(matchguad[-1:])[2:-2]}€",color="blue",marker='o')
        gplt.scatter(bestdate,(np.max(listguadagni)),s=125,label=f"Best Earnings Portfolio: {np.max(listguadagni)}")
        gplt.set_xlabel(f'Date\nfrom {stockdf[0]["Date"][0]} to {stockdf[0]["Date"][maxtime-1]}') 
        gplt.legend(frameon=False)
        
        # fig.legend(loc="lower left", title="", frameon=False)
        fig.tight_layout(h_pad=-1)
        plt.gcf().autofmt_xdate()
        plt.show()
    else:
        return print("Files are not compatible")

def genlistavgtuple(logbpathfolder,logbnames): # Returns a list of tuples with all risk and return avg of all files 
    listavgtuple=[]
    for dump in logbnames:
        logbpathfile=os.path.join(logbpathfolder, dump)+'.dump'
        logbooks=pickle.load(open(logbpathfile,"rb"))
        listavgyield=[]
        listavgrisk=[]
        for logb in logbooks:
            for stat in logb:
                avgrisk=stat["avg"][0]
                avgyield=stat["avg"][1]
                listavgrisk.append(avgrisk)
                listavgyield.append(avgyield)
        listavgtuple.append([np.mean(listavgrisk),np.mean(listavgyield)])

    return listavgtuple

def findbestconfig(logbpathfolder,logbnames): # Returns the best configurations for minimum risk and maximum return among all files
    maxyield=0
    minrisk=1
    for dump in logbnames:
        logbpathfile=os.path.join(logbpathfolder, dump)+'.dump'
        logbooks=pickle.load(open(logbpathfile,"rb"))
        for logb in logbooks:
            for stat in logb:
                avgrisk=stat["avg"][0]
                avgyield=stat["avg"][1]
                if avgrisk<minrisk:
                    minrisk=avgrisk
                    relativeyield=avgyield
                    configminrisk=logbpathfile[logbpathfile.find("Logb"):-5]
                if avgyield>maxyield:
                    maxyield=avgyield
                    relativerisk=avgrisk
                    configmaxyield=logbpathfile[logbpathfile.find("Logb"):-5]
    bestconfigrisk=[[configminrisk,minrisk,relativeyield]]
    bestconfigyield=[[configmaxyield,maxyield,relativerisk]]
    return (bestconfigrisk,bestconfigyield)
    
def main():
    global scelta
    scelta=-1
    bestconfigriskmon,bestconfigyieldmon=findbestconfig(PATHLOGBMONFOLDER,gendumpnames(PATHLOGBMONFOLDER))
    bestconfigrisktrim,bestconfigyieldtrim=findbestconfig(PATHLOGBTRIFOLDER,gendumpnames(PATHLOGBTRIFOLDER))
    print('\nBest portfolios found among MONTHLY configurations:')
    print(f'MIN RISK: {bestconfigriskmon[0][1]} with yield {bestconfigriskmon[0][2]} - configuration {bestconfigriskmon[0][0]}')
    print(f'MAX YIELD: {bestconfigyieldmon[0][1]} with risk {bestconfigyieldmon[0][2]} - configuration {bestconfigyieldmon[0][0]}')
    print('\nBest portfolios found among TRIMESTRAL configurations:')
    print(f'MIN RISK: {bestconfigrisktrim[0][1]} with yield {bestconfigrisktrim[0][2]} - configuration {bestconfigrisktrim[0][0]}')
    print(f'MAX YIELD: {bestconfigyieldtrim[0][1]} with risk {bestconfigyieldtrim[0][2]} - configuration {bestconfigyieldtrim[0][0]}')
    while(not scelta==0):
        tkChooseButton()
        if scelta==1:
            tkloadmensile(gendumpnames(PATHLOGBMONFOLDER),gendumpnames(PATHGUADMONFOLDER))
        elif scelta==2:
            tkloadtrimestrale(gendumpnames(PATHLOGBTRIFOLDER),gendumpnames(PATHGUADTRIFOLDER))

if __name__ == "__main__":
    stockdf,stocknames= genstockdf(PATHCSVFOLDER)
    main()
                        
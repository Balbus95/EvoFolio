### 1) prima di entrare nel tournmantet verifico budget >100000 e scarto tutti quelli che l'hanno superato
### 2) lanciare nsga2 senza partire con random al secondo giro

import random
import time as tm
import os
import itertools as iter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from deap import creator, base, tools, algorithms

def isWindows():
    return os.name=="nt"

ABSPATH=os.path.dirname(os.path.abspath(__file__))

if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix

#PATHCSV1=PATHCSVFOLDER+"\\AAPL.csv"
#PATHCSV2=PATHCSVFOLDER+"\\AAPL.csv"
        
    
def main():
    stockdf,stocknames = genstockdf()
    individual=[1,1,1,1,1,1,1,1]
    maxtime=len(stockdf[0])
    valorimid=[]
    valorimin=[]
    valorimax=[]
    # individual=[14,11,5,21,11,21,14,1]
    # individual=[2,2,2,2,2,2,2,2]
    # sortedList = os.listdir(PATHCSVFOLDER) 
    # sortedList.sort()
    # for stock in sortedList: #per ogni file nella cartella myFolder
    #     stocknames.append(stock[:-4]) # ci metto il nome del file senza i quattro caratteri finali cioè .csv
    #     azioni = int(input(f'Quante azioni hai di {stock[:-4]} ? ')) #per mettere il numero di azioni da tastiera
    #     individual.append(azioni)
    # maxtime=3
    if(len(stocknames)==len(individual)==len(stockdf)):
        for time in range(1,maxtime+1): #arriva alla riga del csv time-1 min=1 max 153 per WEEK 738 per DAY (NUMERO DI RIGHE DA PRENDERE)
            data=str(pd.to_datetime(stockdf[0]["Date"][time-1]))[:-9] # -9 taglia i caratteri dei hh:mm:ss dalla stringa
            print(f"\n################################################ {data} ### {time} #############################################################")
            print(f"STOCK NAMES: {stocknames}")
            print(f"AZIONI POSSEDUTE: {individual}")
            print(f"LISTA NOMI == DA AZIONI == STOCK AZIONI ({len(stocknames)} == {len(individual)} == {len(stockdf)})")
            
            totrisk,totyield=myfitness(stockdf,stocknames,individual,time)

            print("--------------------------------------")
            print(f'MYFITNESS: \nYIELD: {totyield} \nRISK: {totrisk}')
            print("--------------------------------------")

            mincost=lucky(stockdf,individual,time)
            avgcost=middle(stockdf,individual,time)
            maxcost=murphy(stockdf,individual,time)
            valorimin.append(mincost)
            valorimid.append(avgcost)
            valorimax.append(maxcost)
            print("Budget speso:")
            print(f'min: {mincost}')
            print(f'avg: {avgcost}')
            print(f'max: {maxcost}')
            print("--------------------------------------")
            # tm.sleep(5)

            # closecost=totbycol(stockdf,individual,time,"Close")
            # print(f'tot close: {closecost}')

            # df1=pd.read_csv(PATHCSV1,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
            # df2=pd.read_csv(PATHCSV2,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])

            # df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=["Open", "High", "Low"])
            # df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=[1,2,3,4,5])
            
            # date.append(stockdf[0]["Date"][time-1])


        
        
        date=pd.to_datetime(stockdf[0]["Date"]) 
        # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=6))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
        plt.plot(date,valorimax,label="max",color="red")
        plt.plot(date,valorimid,label="mid",color="blue")
        plt.plot(date,valorimin,label="min",color="green")
        plt.title(f"Portfolio {individual}")
        plt.xlabel("Data")
        plt.xticks(rotation=20)
        plt.ylabel("Valore")
        plt.legend()
        # plt.grid()
        # plt.gcf().autofmt_xdate()
        plt.show()   


    else:
        print(f"ERRORE: Lunghezza stocknames,individual,stockdf ({len(stocknames)}!={len(individual)}!={len(stockdf)})")


def myfitness(stockdf,stocknames,individual,time): #individual
    totyield=0
    listvar=[]
    listrisk=[]
    comb=combinator(len(stocknames))
    for i in range(len(stocknames)):
        df=stockdf[i]
        listyeld=calcyield(df,"Close",time)
        listvar.append(np.var(listyeld))
        totyield += individual[i]*np.average(listyeld)
        # print(f"AVG: {np.average(listyeld)} totalyeld {totyield}")
    for coppia in comb:
        x=coppia[0]
        y=coppia[1]
        df1=stockdf[x]
        df2=stockdf[y]
        listyeld1=calcyield(df1,"Close",time)
        listyeld2=calcyield(df2,"Close",time)
        # cov=calccov(df1,df2,"Close",time) #VEDERE SE È GIUSTO
        cov=calccov(listyeld1,listyeld2,time)
        # print(f'{coppia},{individual[x]/sum(individual)}, {sum(individual)}')
        risk=calcrisk(individual[x]/sum(individual),individual[y]/sum(individual),listvar[x],listvar[y],cov)
        listrisk.append(risk)
    # print(f"listvar {listvar}")
    # print(listrisk) 
    # print(sum(listrisk)) 
    totrisk=sum(listrisk)
    return (totrisk,totyield)

def middle(stockdf,individual,time):
    avgtotal=0
    for i in range(len(stockdf)):
            low = (stockdf[i]["Low"][time-1])*individual[i]
            high = (stockdf[i]["High"][time-1])*individual[i]
            avg=(low+high)/2
            # print(f"avg {high} + {low} /2 = {avg}")
            avgtotal+=avg
    # print(f"avgtotal: {avgtotal}")
    return avgtotal

def lucky(stockdf,individual,time):
    lowtotal=0
    for i in range(len(stockdf)):
            low = (stockdf[i]["Low"][time-1])*individual[i]
            # print(f"Low {low}")
            lowtotal+=low
    # print(f"lowtotal: {lowtotal}")
    return lowtotal

def murphy(stockdf,individual,time):
    hightotal=0
    for i in range(len(stockdf)):
            high = (stockdf[i]["High"][time-1])*individual[i]
            # print(f"High {high}")
            hightotal+=high
    # print(f"hightotal: {hightotal}")
    return hightotal

def calcrisk(az1,az2,var1,var2,cov):
    risk=(az1*var1)+(az2*var2)+(2*(az1*az2*cov))
    return risk

def calccov(list1,list2,time):
    if time>=3:
        cov=np.cov(list1,list2)
        cov=float(cov[1][0])
        # print(f"l1 {list1} l2 {list2} cov {cov}")
        return cov
    else:
        return 0 #controllare se è giusto!!!!!!!!!!!

def calccovdf(df1,df2,col,time): #non usato
    if time>=2:
        list1=df1[col].values.tolist()
        list2=df2[col].values.tolist()
        cov=np.cov(list1[:time],list2[:time])
        cov=float(cov[1][0])
        # print(f"{col} cov: {cov}")
        return cov
    else: 
        # print(f"calccov: time è minore di 2")
        return 0


def calcyield(df,col,time): #individual è il numero di azioni possedute di quella azione è un indice di individual[]
    yeld=[]
    if time>=2:
        for i in reversed(range(1,len(df[col][:time]))):
            yeld.append(np.log(df[col][time-i]/df[col][time-i-1]))
            # print(i)
            # print(f'{df[col][time-i]} "+" {df[col][time-i-1]}')
            # print(f"{col} YIELD: {yeld}")
        return yeld
    else: 
        # print("calcyield: time è minore di 2")
        yeld=[0]
        return yeld
    
def combinator(len):
    comb=[]
    for i in range(len):
        comb.append(i)
    comb=list(iter.combinations(comb, 2))
    return comb

def genstockdf():
    stockdf=[]
    stocknames=[]
    i=0
    for stock in os.listdir(PATHCSVFOLDER):
        stocknames.append(stock[:-4])
        path=os.path.join(PATHCSVFOLDER, stocknames[i]+'.csv')
        df=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
        stockdf.append(df)
        i+=1
    return (stockdf,stocknames)

#-------------------------------------------------------------------------------------------------------------------------#

def calcdevstd(df,col,time): #non serve
    if time>=2:
        list=df[col].values.tolist()
        std=np.std(list[:time])
        #print(f'{list[time-1]} "+" {std}')
        #print(f"{col} DEV STD: {std}")
        return std
    else: 
        #print(f"calcdevstd: time è minore di 2")
        return 0

def totbycol(stockdf,individual,time,col): #non usato
    totalcost=0
    for i in range(len(stockdf)):
            cost = (stockdf[i][col][time-1])*individual[i]
            #print(f"Close {cost}")
            totalcost+=cost
    return totalcost

def genrisk(stockdf,individual,listvar,col,time): #non serve
    listrisk=[]
    comb=combinator(len(stockdf))
    for coppia in comb:
        x=coppia[0]
        y=coppia[1]
        df1=stockdf[x]
        df2=stockdf[y]
        cov=calccov(df1,df2,col,time)
        risk=calcrisk(individual[x]/sum(individual),individual[y]/sum(individual),listvar[x],listvar[y],cov)
        listrisk.append(risk)
        #print(f"coppia: {coppia} x:{x}, y:{y}")
    #print(f"LISTA RISK:\n{listrisk}")
    totrisk=sum(listrisk)
    return totrisk

def genlistcov(stockdf,col,time):  #non serve
    listcov=[]
    comb=combinator(len(stockdf))
    for coppia in comb:
        x=coppia[0]
        y=coppia[1]
        df1=stockdf[x]
        df2=stockdf[y]
        listcov.append(calccov(df1,df2,col,time))
        #print(f"coppia: {coppia} x:{x}, y:{y}")
    return listcov

def genliststd(stockdf,col,time):  #non serve
    liststd=[]
    for df in stockdf: #per ogni file nella cartella myFolder
       liststd.append(calcdevstd(df,col,time))
    #print(listdevclose)
    return liststd

def genlistyield(stockdf,individual,col,time):  #non serve e non funziona
    listyield=[]
    i=0
    for df in stockdf: #per ogni file nella cartella myFolder
        listyield.append(calcyield(df,individual[i],col,time))
        i+=1
    #print(listyield)
    return listyield

def getcolfromfile(portfolio,index,col):  #non serve
    list=[]
    for stock in os.listdir(PATHCSVFOLDER):
        if portfolio[index]==stock[:-4]:
            path=os.path.join(PATHCSVFOLDER, stock)
            df=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
            list=df[col].values.tolist()
            return list

def getdfbyindex(stocknames,index,col=None): #non serve
    #for stock in os.listdir(PATHCSVFOLDER): 
    #    names.append(stock[:-4])
    path=os.path.join(PATHCSVFOLDER, stocknames[index]+'.csv')
    df=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
    if col!=None:
        list=[]
        list=df[col].values.tolist()
        return list
    return df

def calcyieldold(ultimo,penultimo,azioniposs):  #non usato
    yeld = azioniposs * np.log(ultimo/penultimo)
    return yeld

def addpath(folder,file):  #non usato
    path=folder+'\\'+file
    return path

def path(): #non usato
    for filename in os.listdir(PATHCSVFOLDER):
        f = os.path.join(PATHCSVFOLDER, filename)
        if os.path.isfile(f):
            print(f)

def maxyield(): #non usato
    return random.randint(0,100)

def minrisk(): #non usato
    return random.randint(0,100)

def generacosto(): #non usato
    return random.randint(0,1000)

def topercento(perc):  #non usato
    percf= f"{perc}%"
    return percf

def tofloat(str): #non usato
    str=str.replace(",", "." )
    str=str.strip(" $")
    str=float(str)
    return str

def toeuro(euro):  #non usato
    eurof= f"{euro}€"
    return eurof

def gentitle(numazioni):  #non usato
    title=f"{numazioni} AZIONI"
    return title

def generaportfolio(name,value): #non usato
    title=gentitle(len(name))
    print(f'{title:-^69}')
    print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format('Nome','Possedute','Costo','Guadagno','Rischio'))
    if len(name)==len(value):
        for i in range(len(name)):
            cost= toeuro(generacosto())
            yeld= topercento(maxyield())
            risk= topercento(minrisk())
            print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format(name[i],value[i],cost,yeld,risk))

def genport2(lista): #non usato
    title=gentitle(len(lista))
    print(f'{title:-^69}')
    print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format('Nome','Possedute','Costo','Guadagno','Rischio'))
    for y in lista:
        name,value=y
        cost= toeuro(generacosto())
        yeld= topercento(maxyield())
        risk= topercento(minrisk())
        print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format(name,value,cost,yeld,risk))

def file_is_hidden(p): #non usato
    if isWindows():
        import win32api, win32con
        attribute = win32api.GetFileAttributes(p)
        print(attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM))
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        #print(p)
        #print(p.startswith('.'))
        return p.startswith('.') #linux-osx
 

if __name__ == "__main__":
    main()







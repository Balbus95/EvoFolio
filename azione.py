### 1) prima di entrare nel tournmantet verifico budget >100000 e scarto tutti quelli che l'hanno superato
### 2) lanciare nsga2 senza partire con random al secondo giro
### 3) tenere conto di quanto valgono le nostre azioni al giorno quindi salvare lista di avg e data giorno

from math import sqrt
import random
import os
import itertools as iter
import pandas as pd
import numpy as np
from deap import creator, base, tools, algorithms
import matplotlib.pyplot as plt

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
    valorimid=[]
    valorimin=[]
    valorimax=[]
    date=[]
    individual=[1,1,1,1,1,1,1,1]
    #individual=[0,0,0,0,0,0,0,0,0,0]
    #individual=[1,1,9,1,1,1,1,1,1,1]
    #individual=[14,11,133,21,11,21,14,1,14,14]
    #individual=[2,2,2,2,2,2,2,2]
    maxtime=len(stockdf[0])
    #maxtime=2
    #stocknames=[]
    #individual=[]
    #sortedList = os.listdir(PATHCSVFOLDER) 
    #sortedList.sort()
    # if not (isWindows()):
    #     sortedList=[sortedList for sortedList in os.listdir('./stock/WEEK') if not file_is_hidden(sortedList)]
    #     print(sortedList,"sort")
    #for stock in sortedList: #per ogni file nella cartella myFolder
    #    stocknames.append(stock[:-4]) # ci metto il nome del file senza i quattro caratteri finali cioè .csv
        #azioni = int(input(f'Quante azioni hai di {stock[:-4]} ? ')) #per mettere il numero di azioni da tastiera
        #individual.append(azioni)
    #print(stockdf)
    if(len(stocknames)==len(individual)==len(stockdf)):
        for time in range(1,maxtime+1): #arriva alla riga del csv time-1 min=1 max 153 per WEEK 738 per DAY (NUMERO DI RIGHE DA PRENDERE)
            print(f"\n################################################ TIME {time} #############################################################")
            print(f"STOCK NAMES: {stocknames}")
            print(f"AZIONI POSSEDUTE: {individual}")
            print(f"LISTA NOMI == DA AZIONI == STOCK AZIONI ({len(stocknames)} == {len(individual)} == {len(stockdf)})")
            
            liststd=genliststd(stockdf,"Close",time)
            #listpearson=genlistpearson(stockdf,"Close",time)
            totrisk,totyield=myfitness(stockdf,stocknames,individual,time)

            print("--------------------------------------")
            print(f"SOMMA STD ({len(liststd)}): {sum(liststd)}")
            #print(f"SOMMA PEARSON ({len(listpearson)}): {sum(listpearson)}")
            print("--------------------------------------")
            print(f'MYFITNESS: \nTOT YIELD: {totyield} \n% RISK: {totrisk}')
            print("--------------------------------------")

            print("Budget speso:")
            luckycost=lucky(stockdf,individual,time)
            middlecost=middle(stockdf,individual,time)
            murphycost=murphy(stockdf,individual,time)
            print(f'min: {luckycost}')
            print(f'avg: {middlecost}')
            print(f'max: {murphycost}')
            #closecost=totbycol(stockdf,individual,time,"Close")
            #print(f'tot close: {closecost}')

            #listyield=genlistyield(stockdf,individual,"Close",time)

            # print("\n")
            # print("LISTA STD:")
            # print("LISTA YIELD:")
            # print(listyield)
            # print("LISTA PEARSON:")
            #risk=genrisk(stockdf,individual,liststd,"Close",time)
            
            # print("--------------------------------------\n")
            # print(combinator(len(individual)))
            # print("\n")
            
            # print(f"SOMMA YIELD: {len(listyield)}")
            # print(sum(listyield))
            #print(liststd)
            #print(listpearson)
            #print(f"% RISK: \n{risk}")

            #risk=calcrisk(1,2,46.39180962,15.77973384,-0.248616759)
            #print(risk)

            #azioniposs=individual[0] #1
            

            #df1=pd.read_csv(PATHCSV1,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
            #df2=pd.read_csv(PATHCSV2,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])

            #df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=["Open", "High", "Low"])
            #df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=[1,2,3,4,5])
            date.append(stockdf[0]["Date"][time-1])
            valorimin.append(luckycost)
            valorimid.append(middlecost)
            valorimax.append(murphycost)


        
        plt.plot(date,valorimax,label="max",color="red")
        plt.plot(date,valorimid,label="mid",color="blue")
        plt.plot(date,valorimin,label="min",color="green")
        plt.title(f"Portfolio {individual}")
        plt.xlabel("Data")
        plt.ylabel("Valore")
        plt.legend()
        # plt.grid()
        plt.show()   


    else:
        print(f"ERRORE: Lunghezza stocknames,individual,stockdf ({len(stocknames)}!={len(individual)}!={len(stockdf)})")


def myfitness(stockdf,stocknames,individual,time): #individual
    totyield=0
    liststd=[]
    listrisk=[]
    comb=combinator(len(stocknames))
    for i in range(len(stocknames)):
        df=stockdf[i]
        yeld=calcyield(df,individual[i],"Close",time)
        liststd.append(calcdevstd(df,"Close",time))
        totyield += yeld
    for coppia in comb:
        x=coppia[0]
        y=coppia[1]
        df1=stockdf[x]
        df2=stockdf[y]
        pearson=calcpearson(df1,df2,"Close",time)
        risk=calcrisk(individual[x],individual[y],liststd[x],liststd[y],pearson)
        listrisk.append(risk)
    # print(listrisk) 
    # print(sum(listrisk)) 
    totrisk=sqrt(sum(listrisk)) #SE ESCE UN NUMERO NEGATIVO DALLA SOMMA DÀ ERRORE
    return (totrisk,totyield)

def middle(stockdf,individual,time):
    avgtotal=0
    for i in range(len(stockdf)):
            low = (stockdf[i]["Low"][time-1])*individual[i]
            high = (stockdf[i]["High"][time-1])*individual[i]
            avg=(low+high)/2
            #print(f"avg {high} + {low} /2 = {avg}")
            avgtotal+=avg
    #print(f"avgtotal: {avgtotal}")
    return avgtotal

def lucky(stockdf,individual,time):
    lowtotal=0
    for i in range(len(stockdf)):
            low = (stockdf[i]["Low"][time-1])*individual[i]
            #print(f"Low {low}")
            lowtotal+=low
    #print(f"lowtotal: {lowtotal}")
    return lowtotal

def murphy(stockdf,individual,time):
    hightotal=0
    for i in range(len(stockdf)):
            high = (stockdf[i]["High"][time-1])*individual[i]
            #print(f"High {high}")
            hightotal+=high
    #print(f"hightotal: {hightotal}")
    return hightotal

def calcrisk(az1,az2,std1,std2,pearson):
    risk=az1*az2*std1*std2*pearson
    return risk

def calcpearson(df1,df2,col,time):
    if time>=2:
        list1=df1[col].values.tolist()
        list2=df2[col].values.tolist()
        pearson=np.corrcoef(list1[:time],list2[:time])
        pearson=float(pearson[1][0])
        #print(f"{col} pearson: {pearson}")
        return pearson
    else: 
        #print(f"calcpearson: time è minore di 2")
        return 0

def calcdevstd(df,col,time): #time - indice dove finisce il conto
    if time>=2:
        list=df[col].values.tolist()
        std=np.std(list[:time])
        #print(f'{list[time-1]} "+" {std}')
        #print(f"{col} DEV STD: {std}")
        return std
    else: 
        #print(f"calcdevstd: time è minore di 2")
        return 0

def calcyield(df,individual,col,time): #individual è il numero di azioni possedute di quella azione è un indice di individual[]
    if time>=2:
        yeld = individual * np.log(df[col][time-1]/df[col][time-2])
        #print(f'{df[col][time-1]} "+" {df[col][time-2]}')
        #print(f"{col} YIELD: {yeld}")
        return yeld
    else: 
        #print("calcyield: time è minore di 2")
        return 0
    
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

def totbycol(stockdf,individual,time,col): #non usato
    totalcost=0
    for i in range(len(stockdf)):
            cost = (stockdf[i][col][time-1])*individual[i]
            #print(f"Close {cost}")
            totalcost+=cost
    return totalcost

def genrisk(stockdf,individual,liststd,col,time): #non serve
    listrisk=[]
    comb=combinator(len(stockdf))
    for coppia in comb:
        x=coppia[0]
        y=coppia[1]
        df1=stockdf[x]
        df2=stockdf[y]
        pearson=calcpearson(df1,df2,col,time)
        risk=calcrisk(individual[x],individual[y],liststd[x],liststd[y],pearson)
        listrisk.append(risk)
        #print(f"coppia: {coppia} x:{x}, y:{y}")
    #print(f"LISTA RISK:\n{listrisk}")
    totrisk=sqrt(sum(listrisk))
    return totrisk

def genlistpearson(stockdf,col,time):  #non serve
    listpearson=[]
    comb=combinator(len(stockdf))
    for coppia in comb:
        x=coppia[0]
        y=coppia[1]
        df1=stockdf[x]
        df2=stockdf[y]
        listpearson.append(calcpearson(df1,df2,col,time))
        #print(f"coppia: {coppia} x:{x}, y:{y}")
    return listpearson

def genliststd(stockdf,col,time):  #non serve
    liststd=[]
    for df in stockdf: #per ogni file nella cartella myFolder
       liststd.append(calcdevstd(df,col,time))
    #print(listdevclose)
    return liststd

def genlistyield(stockdf,individual,col,time):  #non serve
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







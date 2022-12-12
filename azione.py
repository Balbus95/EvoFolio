import math
import random
import os
import itertools as iter
import pandas as pd
import numpy as np
from deap import creator, base, tools, algorithms

if os.name == 'nt':
    import win32api, win32con

def isWindows():
    return os.name=="nt"

def file_is_hidden(p):
    if os.name== 'nt':
        attribute = win32api.GetFileAttributes(p)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        print(p)
        print(p.startswith('.'))
        return p.startswith('.') #linux-osx
        file_list = [f for f in os.listdir('./stock/WEEK') if not file_is_hidden(f)]
        print("----dd-d-d-d-d-")
        print(file_list)

ABSPATH=os.path.dirname(os.path.abspath(__file__))
PATHCSVFOLDER=''

if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK"
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK"

PATHCSV1=PATHCSVFOLDER+"/AAPL.csv"
PATHCSV2=PATHCSVFOLDER+"/AAPL.csv"
        
    

def genlistrisk(azioniposs,liststd,col): 
    listrisk=[]
    comb=combinator(len(azioniposs))
    x=comb[0][0]
    y=comb[0][1]
    for coppia in comb:
        x=coppia[0]
        y=coppia[1]
        df1=getdfbyindex(x)
        df2=getdfbyindex(y)
        pearson=calcpearson(df1,df2,col)
        risk=calcrisk(azioniposs[x],azioniposs[y],liststd[x],liststd[y],pearson)
        listrisk.append(risk)
        #print(f"coppia: {coppia} x:{x}, y:{y}")
    return listrisk

def genlistpearson(col,len):
    listpearson=[]
    comb=combinator(len)
    x=comb[0][0]
    y=comb[0][1]
    for coppia in comb:
        x=coppia[0]
        y=coppia[1]
        df1=getdfbyindex(x)
        df2=getdfbyindex(y)
        listpearson.append(calcpearson(df1,df2,col))
        #print(f"coppia: {coppia} x:{x}, y:{y}")
    return listpearson

def genlistyield(col,azioniposs):
    listyield=[]
    i=0
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        path=os.path.join(PATHCSVFOLDER, stock)
        stock=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
        listyield.append(calcyield(stock,azioniposs[i],col))
        i+=1
    #print(listyield)
    return listyield

def genliststd(col):
    liststd=[]
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        path=os.path.join(PATHCSVFOLDER, stock)
        stock=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
        liststd.append(calcdevstd(stock,col))
    #print(listdevclose)
    return liststd

def getdfbyindex(index):
    names=[]
    for stock in os.listdir(PATHCSVFOLDER): 
        names.append(stock[:-4])
    for stock in os.listdir(PATHCSVFOLDER): 
        if names[index]==stock[:-4]:
            path=os.path.join(PATHCSVFOLDER, stock)
            df=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
            return df

def getcolfromfile(portfolio,index,col):
    list=[]
    for stock in os.listdir(PATHCSVFOLDER):
        if portfolio[index]==stock[:-4]:
            path=os.path.join(PATHCSVFOLDER, stock)
            df=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
            list=df[col].values.tolist()
            return list

def calcrisk(az1,az2,std1,std2,pearson):
    risk=az1*az2*std1*std2*pearson
    return risk

def calcpearson(df1,df2,col):
    list1=df1[col].values.tolist()
    list2=df2[col].values.tolist()
    pearson=np.corrcoef(list1,list2)
    pearson=float(pearson[1][0])
    #print(f"{col} pearson: {pearson}")
    return pearson

def calcdevstd(df,col):
    list=df[col].values.tolist()
    std=np.std(list)
    #print(f"{col} DEV STD: {std}")
    return std

def calcyield(df,azioniposs,col):
    i=df.last_valid_index()
    yeld = azioniposs * np.log(df[col][i]/df[col][i-1])
    #print(f"{col} YIELD: {yeld}")
    return yeld

def combinator(len):
    comb=[]
    for i in range(len):
        comb.append(i)
    comb=list(iter.combinations(comb, 2))
    return comb

def calcyieldold(ultimo,penultimo,azioniposs):
    yeld = azioniposs * np.log(ultimo/penultimo)
    return yeld

def addpath(folder,file):
    path=folder+'\\'+file
    return path

def path():
    for filename in os.listdir(PATHCSVFOLDER):
        f = os.path.join(PATHCSVFOLDER, filename)
        if os.path.isfile(f):
            print(f)

def tofloat(str):
    str=str.replace(",", "." )
    str=str.strip(" $")
    str=float(str)
    return str

def maxyield():
    return random.randint(0,100)

def minrisk():
    return random.randint(0,100)

def generacosto():
    return random.randint(0,1000)

def topercento(perc):
    percf= f"{perc}%"
    return percf

def toeuro(euro):
    eurof= f"{euro}€"
    return eurof

def gentitle(numazioni):
    title=f"{numazioni} AZIONI"
    return title

def generaportfolio(name,value):
    title=gentitle(len(name))
    print(f'{title:-^69}')
    print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format('Nome','Possedute','Costo','Guadagno','Rischio'))
    if len(name)==len(value):
        for i in range(len(name)):
            cost= toeuro(generacosto())
            yeld= topercento(maxyield())
            risk= topercento(minrisk())
            print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format(name[i],value[i],cost,yeld,risk))

def genport2(lista):
    title=gentitle(len(lista))
    print(f'{title:-^69}')
    print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format('Nome','Possedute','Costo','Guadagno','Rischio'))
    for y in lista:
        name,value=y
        cost= toeuro(generacosto())
        yeld= topercento(maxyield())
        risk= topercento(minrisk())
        print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format(name,value,cost,yeld,risk))

def main():
    PortfolioNames=[]
    #PortfolioValue=[]
    PortfolioValue=[1,2,17,3,4,5,3,1]
    sortedList = os.listdir(PATHCSVFOLDER) 
    print(sortedList,"not sort")
    sortedList.sort()
    sortedList=[sortedList for sortedList in os.listdir('./stock/WEEK') if not file_is_hidden(sortedList)]
    print(sortedList,"sort")
    

    
    for stock in sortedList: #per ogni file nella cartella myFolder
        PortfolioNames.append(stock[:-4]) # ci metto il nome del file senza i quattro caratteri finali cioè .csv
        #azioni = int(input(f'Quante azioni hai di {stock[:-4]} ? ')) #per mettere il numero di azioni da tastiera
        #PortfolioValue.append(azioni)
    print(PortfolioNames)
    print(PortfolioValue)
    
    if(len(PortfolioNames)==len(PortfolioValue)):
        print(f"\nLISTA NOMI == DA AZIONI ({len(PortfolioNames)} != {len(PortfolioValue)})")

        listyield=genlistyield("Close",PortfolioValue)
        liststd=genliststd("Close")
        listpearson=genlistpearson("Close",len(PortfolioValue))
        listrisk=genlistrisk(PortfolioValue,liststd,"Close")


        print("\n")
        print("LISTA YIELD:")
        print(listyield)
        print("LISTA STD:")
        print(liststd)
        print("LISTA PEARSON:")
        print(listpearson)
        print("LISTA RISK:")
        print(listrisk)
        
        print("\n")
        print(combinator(len(PortfolioValue)))
        print("\n")
        
        print(f"SOMMA YIELD: {len(listyield)}")
        print(sum(listyield))
        print(f"SOMMA STD: {len(liststd)}")
        print(sum(liststd))
        print(f"SOMMA PEARSON: {len(listpearson)}")
        print(sum(listpearson))
        print(f"SOMMA RISK: {len(listrisk)}")
        print(sum(listrisk))
        print(f"RADQ SOMMA RISK:\n{math.sqrt(sum(listrisk))}")
        print("\n")

        #risk=calcrisk(1,2,46.39180962,15.77973384,-0.248616759)
        #print(risk)

        #azioniposs=PortfolioValue[0] #1
        

        df1=pd.read_csv(PATHCSV1,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
        df2=pd.read_csv(PATHCSV2,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])

        #df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=["Open", "High", "Low"])
        #df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=[1,2,3,4,5])
    
    
    
    else:
        print(f"ERRORE: LISTA NOMI DIVERSA DA AZIONI ({len(PortfolioNames)} != {len(PortfolioValue)})")
    
 

if __name__ == "__main__":
    main()







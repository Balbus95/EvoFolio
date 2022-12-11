import itertools as iter
import random
import pandas as pd
import numpy as np
from deap import creator, base, tools, algorithms
import os

PATHCSVFOLDER= os.path.abspath(__file__)+"\\stock\\WEEK"
PATHCSV1=PATHCSVFOLDER+"\\AAPL.csv"
PATHCSV2=PATHCSVFOLDER+"\\AMZN.csv"




def genlistyield(col,azioni):
    listyield=[]
    i=0
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        path=os.path.join(PATHCSVFOLDER, stock)
        stock=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
        listyield.append(calcyield(stock,azioni[i],col))
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

def genlistpearson(col):
    listpearson=[]
    comb=combinator()
    x=comb[0][0]
    y=comb[0][1]
    i=0
    for x in range(len(comb)):
        x=comb[x][y]
        print(f"x:{x}, y:{y}")
        """for x,y in comb:
            print(f"x:{x}, y:{y}")
            df1=getdfbyindex(x)
            df2=getdfbyindex(y)
            pearson=calcpearson(df1,df2,col)
            listpearson.append(calcpearson(df1,df2,col))
            print(pearson)
            print(listpearson)"""



def calcpearson(df1,df2,col):
    list1=df1[col].values.tolist()
    list2=df2[col].values.tolist()
    pearson=np.corrcoef(list1,list2)
    pearson=float(pearson[1][0])
    #print(f"{col} pearson: {pearson}")
    return pearson


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

def calcdevstd(df,col):
    list=df[col].values.tolist()
    std=np.std(list)
    #print(f"{col} DEV STD: {std}")
    return std

def calcyield(df,azioni,col):
    i=df.last_valid_index()
    yeld = azioni * np.log(df[col][i]/df[col][i-1])
    #print(f"{col} YIELD: {yeld}")
    return yeld

def combinator():
    comb=[]
    i=0
    for stock in os.listdir(PATHCSVFOLDER):
        comb.append(i)
        i+=1
    comb=list(iter.combinations(comb, 2))
    return comb

def calcyieldold(ultimo,penultimo,azioni):
    yeld = azioni * np.log(ultimo/penultimo)
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
    PortfolioValue=[1,2,17,3,4,5,3,1,0,5]
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        PortfolioNames.append(stock[:-4]) # ci metto il nome del file senza i quattro caratteri finali cioè .csv
        #azioni = int(input(f'Quante azioni hai di {stock[:-4]} ? ')) #per mettere il numero di azioni da tastiera
        #PortfolioValue.append(azioni)

 
    listyield=genlistyield("Close",PortfolioValue)
    listyieldadj=genlistyield("Adj Close",PortfolioValue)

    liststd=genliststd("Close")
    liststdadj=genliststd("Adj Close")

    print(listyield)
    print(listyieldadj)
    print(liststd)
    print(liststdadj)

    azioni=PortfolioValue[0] #1

    print(PortfolioNames)
    print(PortfolioValue)
    #portfolio=[["Apple",1],["Amazon",2],["Tesla",17]]
    df1=pd.read_csv(PATHCSV1,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
    df2=pd.read_csv(PATHCSV2,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
    pearson=calcpearson(df1,df2,"Close")
    print(pearson)
    listpearson=genlistpearson("Close")
    print(listpearson)

    list1=getcolfromfile(PortfolioNames,azioni,"Close")
    #df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=["Open", "High", "Low"])
    #df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=[1,2,3,4,5])
   
 

if __name__ == "__main__":
    main()







import random
import pandas as pd
import numpy as np
from deap import creator, base, tools, algorithms
import os

PATHCSVFOLDER="C:\\Users\\mario\\OneDrive\\Documenti\\GitHub\\evoport\\stock\\WEEK"
PATHCSV1=PATHCSVFOLDER+"\\AAPL.csv"
PATHCSV2=PATHCSVFOLDER+"\\ADBE.csv"


def genlistyield(azioni):
    listyield=[]
    i=0
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        path=addpath(PATHCSVFOLDER,str(stock))
        stock=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
        listyield.append(calcyieldclose(stock,azioni[i]))
        i=i+1
    #print(listyield)
    return listyield

def genlistyieldadj(azioni):
    listyieldadj=[]
    i=0
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        path=addpath(PATHCSVFOLDER,str(stock))
        stock=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
        listyieldadj.append(calcyieldadjclose(stock,azioni[i]))
        i=i+1
    #print(listyieldadj)
    return listyieldadj

def genlistdevclose():
    listdevclose=[]
    i=0
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        path=addpath(PATHCSVFOLDER,str(stock))
        stock=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
        listdevclose.append(calcdevstdclose(stock))
        i=i+1
    #print(listdevclose)
    return listdevclose

def genlistdevadjclose():
    listdevadjclose=[]
    i=0
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        path=addpath(PATHCSVFOLDER,str(stock))
        stock=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
        listdevadjclose.append(calcdevstdadjclose(stock))
        i=i+1
    #print(listdevadjclose)
    return listdevadjclose

def addpath(folder,file):
    path=folder+'\\'+file
    return path

def tofloat(str):
    str=str.replace(",", "." )
    str=str.strip(" $")
    str=float(str)
    return str

def calcpearsonclose(df1,df2):
    list1=df1["Close"].values.tolist()
    list2=df2["Close"].values.tolist()
    pearson=np.corrcoef(list1,list2)
    print(f"Close pearson: {pearson}")
    return pearson

def calcpearsonadjclose(df1,df2):
    list1=df1["Adj Close"].values.tolist()
    list2=df2["Adj Close"].values.tolist()
    pearson=np.corrcoef(list1,list2)
    print(f"Adj Close pearson: {pearson}")
    return pearson 

def calcdevstdclose(df):
    list=df["Close"].values.tolist()
    std=np.std(list)
    #print(f"Close DEV STD: {std}")
    return std

def calcdevstdadjclose(df):
    list=df["Adj Close"].values.tolist()
    std=np.std(list)
    #print(f"Adj Close DEV STD: {std}")
    return std

def calcyield(ultimo,penultimo,azioni):
    yeld = azioni * np.log(ultimo/penultimo)
    return yeld

def calcyieldclose(df,azioni,col="Close"):
    i=df.last_valid_index()
    ultimo = df[col][i]
    penultimo = df[col][i-1]
    #ultimo= tofloat(ultimo)
    #penultimo= tofloat(penultimo)
    yeld = azioni * np.log(ultimo/penultimo)
    #print(f"Close YIELD: {yeld}")
    return yeld

def calcyieldadjclose(df,azioni,col="Adj Close"):
    i=df.last_valid_index()
    ultimo = df[col][i]
    penultimo = df[col][i-1]
    #ultimo= tofloat(ultimo)
    #penultimo= tofloat(penultimo)
    yeld = azioni * np.log(ultimo/penultimo)
    #print(f"Adj Close YIELD: {yeld}")
    return yeld

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
    PortfolioValue=[1,2,17,3,4,5,3,1,0,65]
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        PortfolioNames.append(stock[:-4]) # ci metto il nome del file senza i quattro caratteri finali cioè .csv
        #azioni = int(input(f'Quante azioni hai di {stock[:-4]} ? ')) #per mettere il numero di azioni da tastiera
        #PortfolioValue.append(azioni)

 
    listyield=genlistyield(PortfolioValue)
    listyieldadj=genlistyieldadj(PortfolioValue)
    listdevclose= genlistdevclose()
    listdevadjclose=genlistdevadjclose()

    print(listyield)
    print(listyieldadj)
    print(listdevclose)
    print(listdevadjclose)

    azioni=PortfolioValue[0] #1

    print(PortfolioNames)
    print(PortfolioValue)
    #portfolio=[["Apple",1],["Amazon",2],["Tesla",17]]
    df=pd.read_csv(PATHCSV1,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
    df2=pd.read_csv(PATHCSV2,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])

    #df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=["Open", "High", "Low"])
    #df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=[1,2,3,4,5])
   
 

if __name__ == "__main__":
    main()







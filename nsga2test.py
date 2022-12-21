#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY RRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import array
import itertools as iter
import random
import pandas as pd
import json
import os
import numpy 

from math import sqrt

from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator, base, tools, algorithms

ABSPATH=os.path.dirname(os.path.abspath(__file__))
PATHCSVFOLDER=''


def isWindows():
    return os.name=="nt"

if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix

PATHCSV1=PATHCSVFOLDER+"\\AAPL.csv"
PATHCSV2=PATHCSVFOLDER+"\\AAPL.csv"

creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

# Problem definition
# Functions zdt1, zdt2, zdt3, zdt6 have bounds [0, 1]
BOUND_LOW, BOUND_UP = 0.0, 10.0

# Functions zdt4 has bounds x1 = [0, 1], xn = [-5, 5], with n = 2, ..., 10
# BOUND_LOW, BOUND_UP = [0.0] + [-5.0]*9, [1.0] + [5.0]*9

# Functions zdt1, zdt2, zdt3 have 30 dimensions, zdt4 and zdt6 have 10
NDIM = 2 #dimensione singola tupla default 30

def myfitness(individual,stocknames,time): #portfoliovalue
    totyield=0
    liststd=[]
    listrisk=[]
    comb=combinator(len(stocknames))
    for i in range(len(stocknames)):
        df=getdfbyindex(i,stocknames)
        yeld=calcyield(df,individual[i],"Close",time)
        liststd.append(calcdevstd(df,"Close",time))
        totyield += yeld

    for coppia in comb:
        x=coppia[0]
        y=coppia[1]
        df1=getdfbyindex(x)
        df2=getdfbyindex(y)
        pearson=calcpearson(df1,df2,"Close",time)
        risk=calcrisk(individual[x],individual[y],liststd[x],liststd[y],pearson)
        listrisk.append(risk)    
    totrisk=sqrt(sum(listrisk))
    return (totrisk,totyield)

def uniform(low, up, size=None): #creazione popolazione (funzione base)
    try:
        #print("try ",[random.randint(a,b) for a, b in zip(low, up)])
        return [random.randint(a,b) for a, b in zip(low, up)] #viene ripetuto per MU volte
    except TypeError:  #non so perchè fa 4 giri nell'except, returna al try il numero per NDIM volte 
        #print("catch ",[random.randint(a,b) for a, b in zip([low] * size, [up] * size)])
        return [random.randint(a,b) for a, b in zip([low] * size, [up] * size)]


toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM) #genera numeri
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float) #crea individui con attr_float
toolbox.register("population", tools.initRepeat, list, toolbox.individual) #ripete funzione individual

#toolbox.register("evaluate", myfitness) #funzione fitness
toolbox.register("evaluate", benchmarks.zdt1) #funzione fitness
toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0) #crossover function
toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM) #mutation function
toolbox.register("select", tools.selNSGA2) # funzione di selection nsga2

def main(seed=None):
    random.seed(seed)
    
    NGEN = 50 #numero generazioni
    MU = 200 #generazione tuple population, deve essere multiplo di 4 (Dimensione popolazione)
    CXPB = 0.9

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    pop = toolbox.population(n=MU)
    print(pop)
    print('pop {}: {} '.format(len(pop), pop))

    #  Valutare gli individui con un'idoneità non valida
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    #print('invalid {}: {} '.format(len(invalid_ind), invalid_ind))
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Questo serve solo ad assegnare la distanza di affollamento agli individui
    # non viene effettuata una vera e propria selezione
    pop = toolbox.select(pop, len(pop))
    #print('pop {}: {} '.format(len(pop), pop))


    record = stats.compile(pop) #compile()Applica ai dati della sequenza di input ogni funzione registrata e restituisce i risultati come dizionario. 
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Iniziare il processo generazionale
    for gen in range(1, NGEN):
        # Vary the population
        #scartare individui che costano trobbo con costo>budget

        offspring = tools.selTournamentDCD(pop, len(pop)) 
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):

            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Valutare gli individual con un fitness non valido
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Seleziona la popolazione di nuova generazione
        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop) #compile()Applica ai dati della sequenza di input ogni funzione registrata e restituisce i risultati come dizionario. 
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

    print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

    return pop, logbook


def getdfbyindex(index,stocknames):
    #for stock in os.listdir(PATHCSVFOLDER): 
    #    names.append(stock[:-4])
    path=os.path.join(PATHCSVFOLDER, stocknames[index]+'.csv')
    df=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
    return df

def calcrisk(az1,az2,std1,std2,pearson):
    risk=az1*az2*std1*std2*pearson
    return risk

def calcpearson(df1,df2,col,time):
    list1=df1[col].values.tolist()
    list2=df2[col].values.tolist()
    pearson=numpy.corrcoef(list1[:time-1],list2[:time-1])
    pearson=float(pearson[1][0])
    #print(f"{col} pearson: {pearson}")
    return pearson


def combinator(len):
    comb=[]
    for i in range(len):
        comb.append(i)
    comb=list(iter.combinations(comb, 2))
    return comb

def calcyield(df,stockposs,col,time):
    i=time
    yeld = stockposs * numpy.log(df[col][i]/df[col][i-1])
    #print(f"{col} YIELD: {yeld}")
    return yeld

def calcdevstd(df,col,time): #time - indice dove finisce il conto
    list=df[col].values.tolist()
    std=numpy.std(list[:time-1])
    #print(f"{col} DEV STD: {std}")
    return std

if __name__ == "__main__":
    pop, stats = main()
    budget=100000
    stocknames=[]
    for stock in os.listdir(PATHCSVFOLDER): #per ogni file nella cartella myFolder
        stocknames.append(stock[:-4])
    
    #for time in range(2 ,150): #alla fine di ogni settimana il nostro portafogli da individui tutti uguali al migliore della settimana precedente
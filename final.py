with open('terminalout.txt', 'w') as term, open('log.txt', 'w') as logb:
    
    import random
    import time
    import os
    import itertools as iter
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import array

    from deap.benchmarks.tools import diversity, convergence, hypervolume
    from deap import creator, base, tools

    def isWindows():
        return os.name=="nt"

    ABSPATH=os.path.dirname(os.path.abspath(__file__))

    if(isWindows()): 
        PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
    else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix

    BOUND_LOW, BOUND_UP = 1.0, 10.0
    NDIM = 2 #dimensione singola tupla default 30 # lunghezza portafoglio (numero di azioni disponibili)

    NGEN = 5 #numero generazioni
    MU = 4 #generazione tuple population, deve essere multiplo di 4 (Dimensione popolazione)
    CXPB = 0.9

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

    def printpop(pop):
        print(f"{len(pop)} - ", end='',file=term)
        for i in range(len(pop)):
            print(f"{str(pop[i])[16:-1]}", end=',',file=term)

    def combinator(len):
            comb=[]
            for i in range(len):
                comb.append(i)
            comb=list(iter.combinations(comb, 2))
            return comb

    def uniform(low, up, size=None): #creazione popolazione (funzione base)
        try:
            return [random.randint(a,b) for a, b in zip(low, up)] #viene ripetuto per MU volte
        except TypeError:  #non so perchè fa 4 giri nell'except, returna al try il numero per NDIM volte 
            return [random.randint(a,b) for a, b in zip([low] * size, [up] * size)]

    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti)


    random.seed()
    toolbox = base.Toolbox()
    toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM) #genera numeri
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float) #crea individui con attr_float
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) #ripete funzione individual
    pop = toolbox.population(n=MU)

    stockdf,stocknames = genstockdf()
    comb=combinator(len(stockdf))
    maxtime=len(stockdf[0])

    print(f"STOCK NAMES: {stocknames}",file=term)
    print(f"LISTA NOMI == DA AZIONI == STOCK AZIONI ({len(stocknames)} == {len(pop[0])} == {len(stockdf)})",file=term)
    print(f'\nPOP INIZIALE: ', end='',file=term)
    printpop(pop)
    
    valorimid=[]
    valorimin=[]
    valorimax=[]

    for tempo in range(1,maxtime+1): #arriva alla riga del csv time-1 min=1 max 153 per WEEK 738 per DAY (NUMERO DI RIGHE DA PRENDERE)
        
        time.sleep(1/4)

        def myfitness(individual):
            listvar=[]
            listrisk=[]
            for i in range(len(stocknames)):
                totyield=0
                df=stockdf[i]
                listyeld=calcyield(df,"Close",tempo)
                listvar.append(np.var(listyeld))
                totyield += individual[i]*np.average(listyeld) #chiedere se usare np.mean()!!!!!!!!!!!
                # print(f"AVG: {np.average(listyeld)} totalyeld {totyield}")
            for coppia in comb:
                x=coppia[0]
                y=coppia[1]
                df1=stockdf[x]
                df2=stockdf[y]
                listyeld1=calcyield(df1,"Close",tempo)
                listyeld2=calcyield(df2,"Close",tempo)
                cov=calccov(listyeld1,listyeld2,tempo)
                # print(f'{coppia},({individual[x]}{individual[y]}), {sum(individual)}')
                risk=calcrisk(individual[x]/sum(individual),individual[y]/sum(individual),listvar[x],listvar[y],cov) # crasha se sum(individual)=0
                listrisk.append(risk)
            totrisk=sum(listrisk)
            return (totrisk,totyield)

        toolbox.register("evaluate", myfitness) #funzione fitness
        toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0) #crossover function
        toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM) #mutation function
        toolbox.register("select", tools.selNSGA2) # funzione di selection nsga2

        def main():

            global pop
            
            if(len(stocknames)==len(pop[0])==len(stockdf)):

                data=str(pd.to_datetime(stockdf[0]["Date"][tempo-1]))[:-9] # -9 taglia i caratteri dei hh:mm:ss dalla stringa
                print(f"\n\n\n\n{tempo} ---- {data} ------------------------------------------------",file=term)
                print(f"\n\n\n\n{tempo} ---- {data} ------------------------------------------------",file=logb)
                print(f"{tempo} ---- {data}")


                print(f'\n%%%%%%%%PRIMA NSGA2:',end='',file=term)
                printpop(pop)

                pop=nsga2(pop)
                
                print(f'\n\n%%%%%%%%%DOPO NSGA2:',end='',file=term)
                printpop(pop)

                mincost=lucky(stockdf,pop[0])
                avgcost=middle(stockdf,pop[0])
                maxcost=murphy(stockdf,pop[0])
                valorimin.append(mincost)
                valorimid.append(avgcost)
                valorimax.append(maxcost)
                print("Budget speso:")
                print(f'min: {mincost}')
                print(f'avg: {avgcost}')
                print(f'max: {maxcost}')
                print("--------------------------------------")
                # print(f"{valorimax},{valorimid},{valorimin}")
                return (mincost,avgcost,maxcost)

            else:
                print(f"ERRORE: Lunghezza stocknames,pop,stockdf ({len(stocknames)}!={len(pop[0])}!={len(stockdf)})",file=term)

        def nsga2(pop):
            stats = tools.Statistics(lambda ind: ind.fitness.values)
            stats.register("avg", np.mean, axis=0)
            stats.register("std", np.std, axis=0)
            stats.register("min", np.min, axis=0)
            stats.register("max", np.max, axis=0)

            logbook = tools.Logbook()
            logbook.header = "gen", "evals", "std", "min", "avg", "max"

            #  Valutare gli individui con un'idoneità non valida
            # invalid_ind = [ind for ind in pop]
            invalid_ind = [ind for ind in pop if not ind.fitness.valid] #entra se valid = !False
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses): #viene eseguito solo al primo for
                ind.fitness.values = fit

            # Questo serve solo ad assegnare la distanza di affollamento agli individui
            # non viene effettuata una vera e propria selezione
            pop = toolbox.select(pop, len(pop))

            record = stats.compile(pop) #compile() Applica ai dati della sequenza di input ogni funzione registrata e restituisce i risultati come dizionario. 
            logbook.record(gen=0, evals=len(invalid_ind), **record)
            print(logbook.stream,file=logb)

            print('\n\n\t$$$ Prima di gen',end='',file=term)
            printpop(pop)

            # Iniziare il processo generazionale
            for gen in range(1, NGEN):
                # Vary the population
                #scartare individui che costano trobbo con costo>budget
                
                print(f'\n\t\tiniz gen {gen}: ',end='',file=term)
                printpop(pop)

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
                print(logbook.stream,file=logb)
                
                print(f'\n\t\tfine gen {gen}: ',end='',file=term)
                printpop(pop)
                print('\n',file=term)

            print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]),file=logb)

            print('\n\t$$$$ Fine di gen',end='',file=term)
            printpop(pop)

            return pop

        def middle(stockdf,individual):
            avgtotal=0
            for i in range(len(stockdf)):
                    low = (stockdf[i]["Low"][tempo-1])*individual[i]
                    high = (stockdf[i]["High"][tempo-1])*individual[i]
                    avg=(low+high)/2
                    # print(f"avg {high} + {low} /2 = {avg}")
                    avgtotal+=avg
            # print(f"avgtotal: {avgtotal}")
            return avgtotal

        def lucky(stockdf,individual):
            lowtotal=0
            for i in range(len(stockdf)):
                    low = (stockdf[i]["Low"][tempo-1])*individual[i]
                    # print(f"Low {low}")
                    lowtotal+=low
            # print(f"lowtotal: {lowtotal}")
            return lowtotal

        def murphy(stockdf,individual):
            hightotal=0
            for i in range(len(stockdf)):
                    high = (stockdf[i]["High"][tempo-1])*individual[i]
                    # print(f"High {high}")
                    hightotal+=high
            # print(f"hightotal: {hightotal}")
            return hightotal

        def calcyield(df,col,tempo): #individual è il numero di azioni possedute di quella azione è un indice di individual[]
            yeld=[]
            if tempo>=2:
                for i in reversed(range(1,len(df[col][:tempo]))):
                    yeld.append(np.log(df[col][tempo-i]/df[col][tempo-i-1]))
                    # print(i)
                    # print(f'{df[col][tempo-i]} "+" {df[col][tempo-i-1]}')
                    # print(f"{col} YIELD: {yeld}")
                return yeld
            else: 
                # print("calcyield: tempo è minore di 2")
                yeld=[0]
                return yeld

        def calccov(list1,list2,tempo):
            if tempo>=3:
                cov=np.cov(list1,list2)
                cov=float(cov[1][0])
                # print(f"l1 {list1} l2 {list2} cov {cov}")
                return cov
            else:
                return 0 

        def calcrisk(az1,az2,var1,var2,cov): 
            risk=(az1*var1)+(az2*var2)+(2*(az1*az2*cov)) 
            return risk

        def grafico(valorimin,valorimid,valorimax):
            date=pd.to_datetime(stockdf[0]["Date"]) 
            # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=6))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
            # plt.plot(date,valorimax,label="max",color="red")
            plt.plot(date,valorimid,label="mid",color="blue")
            # plt.plot(date,valorimin,label="min",color="green")
            plt.title(f"Portfolio")
            plt.xlabel("Data")
            plt.xticks(rotation=20)
            plt.ylabel("Valore")
            plt.legend()
            # plt.grid()
            # plt.gcf().autofmt_xdate()
            plt.show()   

        if __name__ == "__main__":
            main()

    # fine for di tempo
    # grafico(valorimin,valorimid,valorimax)

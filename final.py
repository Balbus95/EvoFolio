with open('log.txt', 'w') as log:
    
    import random
    import time
    import os
    import itertools as iter
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import array

    from deap import benchmarks
    from deap.benchmarks.tools import diversity, convergence, hypervolume
    from deap import creator, base, tools, algorithms


    def isWindows():
        return os.name=="nt"

    ABSPATH=os.path.dirname(os.path.abspath(__file__))

    if(isWindows()): 
        PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
    else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix

    BOUND_LOW, BOUND_UP = 0.0, 10.0
    NDIM = 2 #dimensione singola tupla default 30

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

    def combinator(len):
            comb=[]
            for i in range(len):
                comb.append(i)
            comb=list(iter.combinations(comb, 2))
            return comb

    def uniform(low, up, size=None): #creazione popolazione (funzione base)
        try:
            #print("try ",[random.randint(a,b) for a, b in zip(low, up)])
            return [random.randint(a,b) for a, b in zip(low, up)] #viene ripetuto per MU volte
        except TypeError:  #non so perchè fa 4 giri nell'except, returna al try il numero per NDIM volte 
            #print("catch ",[random.randint(a,b) for a, b in zip([low] * size, [up] * size)])
            return [random.randint(a,b) for a, b in zip([low] * size, [up] * size)]

    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti)


    random.seed(3)
    toolbox = base.Toolbox()
    toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM) #genera numeri
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float) #crea individui con attr_float
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) #ripete funzione individual
    pop = toolbox.population(n=MU)

    stockdf,stocknames = genstockdf()
    comb=combinator(len(stockdf))
    maxtime=len(stockdf[0])

    print(f"STOCK NAMES: {stocknames}",file=log)
    print(f"LISTA NOMI == DA AZIONI == STOCK AZIONI ({len(stocknames)} == {len(pop[0])} == {len(stockdf)})",file=log)
    print('POP {}: {} '.format(len(pop), pop),file=log)
    
    valorimid=[]
    valorimin=[]
    valorimax=[]

    for tempo in range(1,maxtime+1): #arriva alla riga del csv time-1 min=1 max 153 per WEEK 738 per DAY (NUMERO DI RIGHE DA PRENDERE)

        def myfitness(individual): #individual
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
                # cov=calccov(df1,df2,"Close",tempo) 
                cov=calccov(listyeld1,listyeld2,tempo) #VEDERE SE È GIUSTO!!!!!!!!!!!!!!!!!!
                # print(f'{coppia},{individual[x]/sum(individual)}, {sum(individual)}')
                risk=calcrisk(individual[x]/sum(individual),individual[y]/sum(individual),listvar[x],listvar[y],cov)
                listrisk.append(risk)
            # print(f"listvar {listvar}")
            # print(listrisk) 
            # print(sum(listrisk)) 
            totrisk=sum(listrisk)
            return (totrisk,totyield)

        toolbox.register("evaluate", myfitness) #funzione fitness
        toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0) #crossover function
        toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM) #mutation function
        toolbox.register("select", tools.selNSGA2) # funzione di selection nsga2

        def main():
            # inditest=[1,1]
            inditest0=[3,9]
            inditest1=[8,2]
            inditest2=[5,9]
            inditest3=[7,10]
            if(len(stocknames)==len(pop[0])==len(stockdf)):
                data=str(pd.to_datetime(stockdf[0]["Date"][tempo-1]))[:-9] # -9 taglia i caratteri dei hh:mm:ss dalla stringa
                print(f"\n################################################ {data} ### {tempo} #############################################################")
                print(f"\n################################################ {data} ### {tempo} #############################################################",file=log)
                # print(f"AZIONI POSSEDUTE: {inditest}")
                
                # totrisk,totyield=myfitness(inditest)
                # totrisk,totyield=myfitness(inditest2)
                # totrisk,totyield=myfitness(inditest3)
                # totrisk,totyield=myfitness(inditest4)
                print(f'IND: \tIND0: {inditest0} \tIND1: {inditest1}\tIND2: {inditest2}\tIND3: {inditest3}',file=log)
                print(f'MYFIT: \tF0: {myfitness(inditest0)} \tF1: {myfitness(inditest1)}\tF2: {myfitness(inditest2)}\tF3: {myfitness(inditest3)}',file=log)
                print("--------------------------------------",file=log)
                # print(f'MYFITNESS: \nYIELD: {totyield} \nRISK: {totrisk}')
                # print("--------------------------------------")

                # time.sleep(1/2)
                nsga2(pop)
                # mincost=lucky(stockdf,inditest)
                # avgcost=middle(stockdf,inditest)
                # maxcost=murphy(stockdf,inditest)
                # valorimin.append(mincost)
                # valorimid.append(avgcost)
                # valorimax.append(maxcost)
                # print("Budget speso:")
                # print(f'min: {mincost}')
                # print(f'avg: {avgcost}')
                # print(f'max: {maxcost}')
                # print("--------------------------------------")
                # print(f"{valorimax},{valorimid},{valorimin}")
                # return (mincost,avgcost,maxcost)

            else:
                print(f"ERRORE: Lunghezza stocknames,individual,stockdf ({len(stocknames)}!={len(pop[0])}!={len(stockdf)})")

        def nsga2(pop):
            
            stats = tools.Statistics(lambda ind: ind.fitness.values)
            stats.register("avg", np.mean, axis=0)
            stats.register("std", np.std, axis=0)
            stats.register("min", np.min, axis=0)
            stats.register("max", np.max, axis=0)

            logbook = tools.Logbook()
            logbook.header = "gen", "evals", "std", "min", "avg", "max"

            #  Valutare gli individui con un'idoneità non valida
            invalid_ind = [ind for ind in pop if not ind.fitness.valid]
            # print('invalid {}: {} '.format(len(invalid_ind), invalid_ind))
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            fit0=myfitness(pop[0])
            fit1=myfitness(pop[1])
            fit2=myfitness(pop[2])
            fit3=myfitness(pop[3])
            print(f"fit0 {fit0},fit1 {fit1},fit2 {fit2},fit3 {fit3}",file=log)
            print(f"pop0 {str(pop[0])[16:-1]},pop1 {str(pop[1])[16:-1]},pop2 {str(pop[2])[16:-1]},pop3 {str(pop[3])[16:-1]}",file=log)
            print("--------------------------------------",file=log)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Questo serve solo ad assegnare la distanza di affollamento agli individui
            # non viene effettuata una vera e propria selezione
            pop = toolbox.select(pop, len(pop))
            print('nsga2 {}: {} \n'.format(len(pop), pop),file=log)


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
                # print('nsga2gen {}: {} '.format(gen, pop),file=log)

            print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

            return (pop,logbook)

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

        def calcrisk(az1,az2,var1,var2,cov): #chiedere covarianza!!!!!!!!!!!!
            risk=(az1*var1)+(az2*var2)+(2*(az1*az2*cov)) 
            return risk

        def grafico(valorimin,valorimid,valorimax):
            date=pd.to_datetime(stockdf[0]["Date"]) 
            # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=6))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
            plt.plot(date,valorimax,label="max",color="red")
            plt.plot(date,valorimid,label="mid",color="blue")
            plt.plot(date,valorimin,label="min",color="green")
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
    #grafico(valorimin,valorimid,valorimax)

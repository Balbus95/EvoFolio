import pickle
import os
import final
from deap import creator, base, tools

stats=pickle.load(open("stats_NGEN=10_CXPB=0.9_SELPARAM=0.8_TOURNPARAM=0.9_MU=48.dump","rb"))
# print(type(stats[0]))

# guadagni=pickle.load(open("guadagni.dump","rb"))
# print(guadagni[0])
listmax=[]
listmin=[]
for i in stats:
    gen, max, min = i.select("gen", "max", "min")
    #print(max)
    #print(max[0][0])
    listmin.append(min)
    listmax.append(max)
    print(str(gen),' ',str(max))
    #print(i)

final.grafico(min,max)
    
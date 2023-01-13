import pickle
import os
from deap import creator, base, tools

# stats=pickle.load(open("MU=1_TOURNPARAM=0.9_SELPARAM=0.8_CXPB=0.9_NGEN=10_guadagni","rb"))
# print(type(stats[0]))

guadagni=pickle.load(open("MU=10_TOURNPARAM=0.9_SELPARAM=0.8_CXPB=0.9_NGEN=10_NDIM=47_guadagni.pkl","rb"))
print(guadagni[0])
print(guadagni)
listmax=[]
listmin=[]
# for i in stats:
#     gen, max, min = i.select("gen", "max", "min")
#     #print(max)
#     #print(max[0][0])
#     listmin.append(min)
#     listmax.append(max)
#     print(str(gen),' ',str(max))
#     #print(i)

# grafico(min,max)
    
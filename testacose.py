import itertools
import os

number = [1,1,1,1,1,1,1]
lista=[]
x=len(number)
i=0
for i in range(x):
    lista.append(i)

print(lista)

print(list(itertools.combinations(lista, 2)))
print(x)

path=os.path.abspath(__file__)
path=path[:5]
print(path)
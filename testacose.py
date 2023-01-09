# with open('filename.txt', 'w') as f:    
#     print("ggg",file=f)
# def calculateSquare(n):
#     return n*n

import final as f

# numbers = (1, 2, 3, 4)
# r = map(calculateSquare, numbers)
# a=r
# print(list(a))
# print(list(r))
# # result.add(5)
# print(r)

stockdf,stocknames = f.genstockdf()
ind=[10,8]
# for i in range(2,10):
mid=f.middle(stockdf,ind)
print(mid)

print("aaaaaaaaaaa")
# converting map object to set
# numbersSquare = set(result)
# print(numbersSquare)


    # for i in range(10):
    #     def f1():
    #         print(f"f1 {i}")
    #         return 1
    #     def f2():
    #         print(f"f2 {i}")
    #         return 0
    #     def main():
    #         f1()
    #         f2()
    #         print(f"main {i}")
    #         return 2

        # if __name__ == "__main__":
        #     main()
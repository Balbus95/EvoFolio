for i in range(10):
    def f1():
        print(f"f1 {i}")
        return 1
    def f2():
        print(f"f2 {i}")
        return 0
    def main():
        f1()
        f2()
        print(f"main {i}")
        return 2

    if __name__ == "__main__":
        main()
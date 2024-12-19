def main():
    mount = 50
    print(f"Amount Due: ${mount}")
    while mount != 0:
        coin = input("Insert Coin: ").strip()
        if coin == "25" or coin == "10" or coin == "5":
            mount = mount - int(coin)
            if(mount <= 0):
                print(f"Change Owed: {mount*(-1)}")
                break
            else:
                print(f"Amount Due: {mount}")
        else:
            print(f"Amount Due: {mount}")


if __name__ == "__main__":
    main()

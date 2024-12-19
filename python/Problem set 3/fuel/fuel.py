def main():
    try:
        data = input("Fraction: ")
        x,y = data.split("/")
        percent = round(int(x)/int(y)*100)
        if int(x)>int(y):
            main()
        elif percent <= 1:
            print(f"E")
        elif percent >= 99:
            print(f"F")
        else:
            print(f"{percent}%")
    except ValueError:
        main()
    except ZeroDivisionError:
        main()

if __name__ == "__main__":
    main()

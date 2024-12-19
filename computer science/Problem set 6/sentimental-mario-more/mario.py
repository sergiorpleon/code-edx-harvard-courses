def main():
    height = 0
    while (True):
        try:
            height = int(input("Height: "))
            if (height >= 1 and height <= 8):
                break
        except ValueError:
            pass

    for i in range(height):
        print(" "*(height-1-i)+"#"*(i+1)+"  "+"#"*(i+1))


if __name__ == "__main__":
    main()

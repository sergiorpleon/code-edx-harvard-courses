import sys

#commnets
def main():
    try:
        if len(sys.argv)<2:
            sys.exit("Too few command-line arguments")
        if len(sys.argv)>2:
            sys.exit("Too many command-line arguments")

        name = sys.argv[1]

        if not name.endswith(".py"):
            sys.exit("Not a Python file")

        count = 0
        with open(name, "r") as file:
            for line in file:
                if not line.strip() == "" and not (line.strip()).startswith("#"):
                    count = count + 1

        print(count)
    except FileNotFoundError:
        sys.exit("File does not exist")

if __name__ == "__main__":
    main()

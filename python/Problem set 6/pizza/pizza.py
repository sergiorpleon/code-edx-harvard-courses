import sys
import csv
from tabulate import tabulate

def main():
    try:
        if len(sys.argv)<2:
            sys.exit("Too few command-line arguments")
        if len(sys.argv)>2:
            sys.exit("Too many command-line arguments")

        name = sys.argv[1]

        if not name.endswith(".csv"):
            sys.exit("Not a CSV file")

        table = []
        with open(name, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                #print(', '.join(row))
                table.append(row)

        print(tabulate(table, headers="firstrow", tablefmt="grid"))
    except FileNotFoundError:
        sys.exit("File does not exist")

if __name__ == "__main__":
    main()

import sys
import csv
from tabulate import tabulate

def main():
    try:
        if len(sys.argv)<3:
            sys.exit("Too few command-line arguments")
        if len(sys.argv)>3:
            sys.exit("Too many command-line arguments")

        name = sys.argv[1]
        output = sys.argv[2]

        if not name.endswith(".csv"):
            sys.exit("Not a CSV file")


        outputfile = open(output, 'w', newline='')
        writer = csv.DictWriter(outputfile, fieldnames=["first", "last", "house"])
        writer.writeheader()
        with open(name, newline='') as csvfile:
            spamreader = csv.DictReader(csvfile)
            for row in spamreader:
                name = row["name"]
                last, first = name.split(",")
                house = row["house"]
                writer.writerow({"first": first.strip(),"last": last.strip(),"house": house.strip()})
        outputfile.close()
    except FileNotFoundError:
        sys.exit(f"Could not read {name}")

if __name__ == "__main__":
    main()

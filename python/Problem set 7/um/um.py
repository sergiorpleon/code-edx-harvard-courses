import re
import sys


def main():
    print(count(input("Text: ")))


def count(s):
    matches = re.findall(r"(\W+|\b)um(\W+|\b)", s.strip().lower())

    return len(matches)

if __name__ == "__main__":
    main()

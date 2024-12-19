from datetime import date
import inflect
import sys

def main():
    try:
        input_date = input("Date: ")

        words = minutes(input_date)

        print(words)
    except ValueError:
        sys.exit("Invalid format")


def minutes(input_date):
    try:
        today = date.today()
        my_date = date.fromisoformat(f"{input_date}")
        current = date.fromisoformat(f"{today.year}-{today.month:02}-{today.day:02}")

        minutes = abs(((current - my_date).days)*24*60)

        p = inflect.engine()
        words = p.number_to_words(minutes, andword="")
        return f"{words.capitalize()} minutes"
    except ValueError:
        raise ValueError


if __name__ == "__main__":
    main()

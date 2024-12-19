import re
import sys


def main():
    try:
        print(convert(input("Hours: ")))
    except ValueError:
        sys.exit("ValueError")

def convert(s):
    #9:00 AM to 5:00 PM
    #9 AM to 5 PM
    #9:00 AM to 5 PM
    #9 AM to 5:00 PM

    matches = re.search(r"^(([0-9]|(1[0-2]))(:[0-5][0-9])? (AM|PM) to ([0-9]|(1[0-2]))(:[0-5][0-9])? (AM|PM))$", s.strip())

    if matches:
        first, second = s.split("to")

        first = get_24_hour(first)
        second = get_24_hour(second)

        return f"{first} to {second}"

    else:
        raise ValueError


def get_24_hour(h):
    time, ampm = h.strip().split(" ")
    if ":" in time:
        hour, min = time.split(":")
    else:
        hour = time
        min = 0

    if hour == "12":
        hour = "0"
    new_hour = int(hour) + (0 if ampm == "AM" else 12)

    return f"{new_hour:02}:{min:02}"




if __name__ == "__main__":
    main()

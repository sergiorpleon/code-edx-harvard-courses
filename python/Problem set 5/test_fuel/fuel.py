
#3-1
def main():
    try:
        data = input("Fraction: ")

        percent = convert(data)
        result = gauge(percent)

        print(result)

    except ValueError:
        main()
    except ZeroDivisionError:
        main()

def convert(fraction):
    try:
        x,y = fraction.split("/")
        percent = round(int(x)/int(y)*100)
        return percent
    except ValueError:
        raise ValueError
    except ZeroDivisionError:
        raise ZeroDivisionError


def gauge(percentage):
    if percentage <= 1:
        return "E"
    elif percentage >= 99:
        return "F"
    else:
        return f"{percentage}%"


if __name__ == "__main__":
    main()

import sys
import inflect



def main():
    names = []

    while True:
        try:
            user_input = input()
            names.append(user_input)

        except KeyError:
            pass
        except EOFError:
            if len(names) > 0:
                print(get_output(names))
            sys.exit()
        except KeyboardInterrupt:
            if len(names) > 0:
                print(get_output(names))
            sys.exit()

def get_output(names):
    p = inflect.engine()
    message = "Adieu, adieu, to "
    return f"{message}{p.join(names)}"

def get_output1(names):
    message = "Adieu, adieu, to "

    if len(names) == 1:
        return message + names[0]

    i = 0
    while i < len(names)-1:
        message = message +("" if i==0 else ", ")+ names[i]
        i = i+1

    message = message +" and " + names[len(names)-1]
    return message

if __name__ == "__main__":
    main()

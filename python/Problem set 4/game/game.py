from random import randint
import sys

def main():
    try:
        n = input("Level: ")
        number = randint(1,int(n))
        print(number)

        while True:
            try:
                user_input = input("Guess: ")
                if int(user_input) > 0:
                    if int(user_input) < number:
                        print("Too small!")
                    elif int(user_input) > number:
                        print("Too large!")
                    else:
                        print("Just right!")
                        sys.exit()
            except ValueError:
                pass
            except EOFError:
                sys.exit()
            except KeyboardInterrupt:
                sys.exit()

    except ValueError:
        main()

if __name__ == "__main__":
    main()

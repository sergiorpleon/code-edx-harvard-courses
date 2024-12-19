import random

def main():
    level = get_level()


    point = 0
    for i in range(10):
        a = generate_integer(level)
        b = generate_integer(level)

        for j in range(3):
            try:
                answer = int(input(f"{a} + {b} = "))
                if answer == a + b:
                    point = point + 1
                    break
                else:
                    print("EEE")
                    if j==2:
                        print(f"{a} + {b} = {a+b}")
            except ValueError:
                print("EEE")
                if j==2:
                    print(f"{a} + {b} = {a+b}")

    print(f"{point}")



def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if level==1 or level==2 or level==3:
                return level
        except ValueError:
            pass

def generate_integer(level):
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(100, 999)

if __name__ == "__main__":
    main()

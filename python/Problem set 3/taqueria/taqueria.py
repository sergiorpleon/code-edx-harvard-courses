
def main():
    menu = {
            "baja taco": 4.25,
            "burrito": 7.50,
            "bowl": 8.50,
            "nachos": 11.00,
            "quesadilla": 8.50,
            "super burrito": 8.50,
            "super quesadilla": 9.50,
            "taco": 3.00,
            "tortilla salad": 8.00
            }

    mount = 0
    while True:
        try:
            user_input = input("Item: ")
            value = menu[user_input.lower()]
            mount = mount + value
            print(f"Total: ${mount:.2f}")
        except KeyError:
            pass
        except EOFError:
            exit()
        except KeyboardInterrupt:
            exit()

if __name__ == "__main__":
    main()

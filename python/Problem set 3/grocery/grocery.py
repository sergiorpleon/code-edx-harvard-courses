def main():
    menu = {

            }
    while True:
        try:
            user_input = input()
            menu[user_input.lower()] = menu[user_input.lower()] + 1

        except KeyError:
            menu[user_input.lower()] = 1
        except EOFError:
            get_output(menu)
            exit()
        except KeyboardInterrupt:
            get_output(menu)
            exit()

def get_output(menu):
    for item in sorted(menu):
        print(f"{menu[item]} {item.upper()}")


if __name__ == "__main__":
    main()

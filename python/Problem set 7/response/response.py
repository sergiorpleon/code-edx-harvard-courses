from validator_collection import validators, checkers, errors



def main():
    is_email = validate(input("Email: "))
    if is_email:
        print("Valid")
    else:
        print("Invalid")


def validate(s):
    try:
        is_email_address = checkers.is_email(s)
        return is_email_address
    except errors.EmptyValueError:
        return False
    except errors.InvalidEmailError:
        return False
    except errors.ValueError:
        return False

if __name__ == "__main__":
    main()

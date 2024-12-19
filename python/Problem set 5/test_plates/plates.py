#2-4
def main():
    text = input("Input: ").strip()

    if is_valid(text):
        print("Valid")
    else:
        print("Invalid")

def is_valid(s):
    if not s.isalnum() or len(s)>6 or len(s)<2:
        return False
    if not s[0].isalpha() or not s[1].isalpha():
        return False

    check_number = False
    for letter in s:
        if check_number and letter.isalpha():
            return False

        if not letter.isalpha() and not check_number:
            if letter == "0":
                return False
            check_number = True

    return True


if __name__ == "__main__":
    main()

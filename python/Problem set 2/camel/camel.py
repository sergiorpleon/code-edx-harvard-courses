def main():
    text = input("Input: ").strip()
    print(convert(text))



def convert(text):
    result = ""
    for letter in text:
        if letter.isupper():
            result = result + "_"
        result = result + letter.lower()
    return result


if __name__ == "__main__":
    main()

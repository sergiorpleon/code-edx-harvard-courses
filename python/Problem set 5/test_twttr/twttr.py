#2-3
def main():
    text = input("Input: ").strip()

    new_word = shorten(text)

    print(f"Output: ${new_word}")

def shorten(word):
    new_word = ""
    for letter in word:
        if not is_aeiou(letter):
            new_word = new_word + letter
    return new_word

def is_aeiou(letter):
    if letter == "a" or letter == "A":
        return True
    elif letter == "e" or letter == "E":
        return True
    elif letter == "i" or letter == "I":
        return True
    elif letter == "o" or letter == "O":
        return True
    elif letter == "u" or letter == "U":
        return True
    else:
        return False


if __name__ == "__main__":
    main()

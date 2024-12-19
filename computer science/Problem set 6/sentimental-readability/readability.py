
def main():
    # Prompt the user for some text
    text = input("Text: ")
    # Count the number of letters, words, and sentences in the text
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Compute the Coleman-Liau index
    L = letters/words*100
    S = sentences/words*100
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Print the grade level
    if (index < 1):
        print("Before Grade 1")
    elif (index == 1):
        print("Grade 1")
    elif (index >= 16):
        print("Grade 16+")
    else:
        print(f"Grade {index}")


"".lower()


def count_letters(text):
    # Return the number of letters in text
    count = 0
    for i in range(len(text)):
        c = text.lower()[i]
        if (c >= 'a' and c <= 'z'):
            count += 1
    return count


def count_words(text):
    # Return the number of words in text
    count = 1
    is_space = False
    for i in range(len(text)):
        if (text[i] == ' '):
            if (not is_space):
                count += 1
            is_space = True
        else:
            is_space = False
    return count


def count_sentences(text):
    # Return the number of sentences in text
    count = 0
    for i in range(len(text)):
        if (text[i] == '.' or text[i] == '!' or text[i] == '?'):
            count += 1
    return count


if __name__ == "__main__":
    main()

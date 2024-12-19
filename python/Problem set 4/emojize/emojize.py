import emoji

def main():
    text = input("Input: ").strip()
    #print(emoji.emojize(text))
    print(emoji.emojize(text, language="alias"))

if __name__ == "__main__":
    main()

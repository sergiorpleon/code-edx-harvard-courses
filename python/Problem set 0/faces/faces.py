def main():
    text = input("Say anything: ")
    print(convert(text))

def convert(words):
    return words.strip().replace(":)", "🙂").replace(":(", "🙁")

main()

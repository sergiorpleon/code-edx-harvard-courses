def main():
    text = input("Say anything: ")
    print(playback(text))

def playback(words):
    return words.strip().replace(" ", "...")

main()

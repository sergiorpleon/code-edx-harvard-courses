from pyfiglet import Figlet
import sys
import random

def main():

    text = ""
    f = Figlet()
    fonts = f.getFonts()

    if len(sys.argv) == 3 and (sys.argv[1]=="-f" or sys.argv[1]=="--font") and sys.argv[2] in fonts:
        f.setFont(font=sys.argv[2])
        text = input().strip()
    elif len(sys.argv)==1:
        font = random.choice(fonts)
        f.setFont(font=font)
        text = input().strip()
    else:
        sys.exit("Invalid usage")

    print(f.renderText(text))


if __name__ == "__main__":
    main()

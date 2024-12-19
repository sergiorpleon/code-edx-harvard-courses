def main():
    text = input("Arithmetic expression: ").strip()
    x, y, z = text.split(" ") if len(text.split(" "))==3 else [0,0,0]
    print(float(interpreter(x, y, z)))

def interpreter(x, y, z):
    if y == "+":
        return int(x)+int(z)
    elif y == "-":
        return int(x)-int(z)
    elif y == "*":
        return int(x)*int(z)
    elif y == "/":
        if z == "0":
            return "Input incorrect"
        else:
            return int(x)/int(z)
    else:
        return "Input incorrect"

main()

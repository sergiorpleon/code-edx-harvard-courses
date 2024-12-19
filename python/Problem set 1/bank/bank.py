def main():
    greeting = input("Greeting: ").strip()
    print(f"${check(greeting)}")

def check(greeting):
    if greeting.lower().startswith("hello"):
        return "$0"
    elif greeting.lower().startswith("h"):
        return "$20"
    else:
        return "$100"

main()

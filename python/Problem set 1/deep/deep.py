def main():
    print("The answer to the big question of life, the universe and everything is?")
    answer = input("Answer: ").strip()

    print(check(answer))

def check(answer):
    if "42" == answer or "forty-two" == answer.lower() or "forty two"  == answer.lower():
        return "Yes"
    else:
        return "No"

main()

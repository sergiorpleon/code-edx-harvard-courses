def main():
    mounth = [
"january",
"february",
"march",
"april",
"may",
"june",
"july",
"august",
"september",
"october",
"november",
"december"
]

    try:
        user_input = input("Date: ").strip()
        if "/" in user_input:
            m, d, y = user_input.split("/")
            y = int(y)
            m = int(m)
            d = int(d)
            if m>12 or m<1 or d<1 or d>31 or len(str(y))!=4:
                main()
            else:
                print(get_output(y, m, d))
        else:
            m, d, y = user_input.split(" ")
            y = int(y)
            m = mounth.index(m.lower())+1
            d = int(d.removesuffix(","))
            if m>12 or m<1 or d<1 or d>31  or len(str(y))!=4 or not "," in user_input:
                main()
            else:
                print(get_output(y, m, d))
    except ValueError:
        main()

def get_output(y, m, d):
    return str(y)+"-"+( "0"+ str(m) if m < 10 else str(m) )+"-"+ ( "0"+str(d) if d < 10 else str(d) )



if __name__ == "__main__":
    main()

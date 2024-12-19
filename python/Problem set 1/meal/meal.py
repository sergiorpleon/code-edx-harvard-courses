def main():
    time = input("Input time: ").strip().lower()
    hour = convert(time)
    if hour >= 7 and hour <= 8:
        print("breakfast time")
    elif hour >= 12 and hour <= 13:
        print("lunch time")
    elif hour >= 18 and hour <= 19:
        print("dinner time")


def convert(time):
    if time.endswith(" a.m."):
        time = time.removesuffix(" a.m.")
        h, m = time.split(":") if len(time.split(":"))==2 else [0,0]
        return float(h)+float(m)/60
    elif time.endswith(" p.m."):
        time = time.removesuffix(" p.m.")
        h, m = time.split(":") if len(time.split(":"))==2 else [0,0]
        return 12+float(h)+float(m)/60
    else:
        h, m = time.split(":") if len(time.split(":"))==2 else [0,0]
        return float(h)+float(m)/60

if __name__ == "__main__":
    main()

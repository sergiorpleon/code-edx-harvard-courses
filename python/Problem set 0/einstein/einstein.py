def main():
    masa = int(input("Input the masa(integer number): "))
    print(calc_energy(masa))

def calc_energy(masa):
    return masa*pow(300000000, 2)

main()

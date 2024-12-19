def main():
    credit = 0

    while True:
        try:
            credit = input("Number: ")
            if int(credit) >= 0:
                break
        except ValueError:
            pass

    value = valid(int(credit))
    print(f"{value}")


def valid(c):
    result = "INVALID\n"

    # count total digit, and get reverse number
    count_digit = 0
    number = c
    reverse = 0
    while (number > 0):
        rest = number % 10
        number = number - rest
        number = int(number / 10)

        reverse = 10*reverse + rest
        count_digit = count_digit + 1

    # 34 == first 2 digit == 37 AMEX len 15
    # 51 <= first 2 digit <= 55 MASTERCARD len 16
    # 4 == first digit VISA 13 == or len == 16

    # check first digit and len of digit
    if ((count_digit == 13 or count_digit == 16) and reverse % 10 == 4):
        result = "VISA"
    elif (count_digit == 15):
        first = reverse % 10
        second = int(((reverse-first)/10) % 10)
        if (first == 3 and (second == 4 or second == 7)):
            result = "AMEX"
        else:
            return "INVALID"

    elif (count_digit == 16):
        first = reverse % 10
        second = int(((reverse-first)/10) % 10)
        if (first == 5 and second >= 1 and second <= 5):
            result = "MASTERCARD"
        else:
            return "INVALID"
    else:
        return "INVALID"

    # check Luhns algorimts conditions
    number = reverse
    print(number)
    i = count_digit % 2
    sum_par = 0
    sum_impar = 0
    while (number > 0):
        rest = number % 10
        number = number - rest
        number = int(number / 10)

        if (i % 2 == 0):
            multi = rest*2
            val = multi % 10
            if (multi >= 10):
                val = val + 1

            sum_par = sum_par + val
        else:
            sum_impar = sum_impar + rest

        i = i + 1

    if ((sum_par + sum_impar) % 10 == 0):
        return result
    else:
        return "INVALID"


def valid1(credit):
    result = "INVALID"

    # 34 <= first 2 digit <= 37 AMEX len 15
    # 51 <= first 2 digit <= 55 MASTERCARD len 16
    # 4 == first digit VISA 13 <= len <= 16

    # check first digit and len of digit
    if len(credit) >= 13 and len(credit) <= 16 and credit[0] == "4":
        result = "VISA"
    elif len(credit) == 15:
        if int(credit[0]) == 3 and int(credit[1]) >= 4 and int(credit[1]) <= 7:
            result = "AMEX"
        else:
            return "INVALID"

    elif len(credit) == 16:
        if int(credit[0]) == 5 and int(credit[1]) >= 1 and int(credit[1]) <= 5:
            result = "MASTERCARD"
        else:
            return "INVALID1"
    else:
        return "INVALID2"

    # check Luhns algorimts conditions
    i = len(credit) % 2
    sum_par = 0
    sum_impar = 0
    for c in credit:

        if i % 2 == 0:
            multi = int(c)*2
            val = multi % 10
            if multi >= 10:
                val = val + 1

            sum_par = sum_par + val
        else:
            sum_impar = sum_impar + int(c)

        i = i + 1

    if ((sum_par + sum_impar) % 10 == 0):
        return result
    else:
        return "INVALID3"


if __name__ == "__main__":
    main()

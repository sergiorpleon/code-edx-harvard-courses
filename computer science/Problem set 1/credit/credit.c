#include <cs50.h>
#include <inttypes.h>
#include <stdio.h>

string valid(long c);

int main(void)
{

    long credit = 0;

    do
    {
        credit = get_long("Number: ");
    }
    while (credit < 0);

    string value = valid(credit);
    printf("%s", value);
}

string valid(long c)
{
    string result = "INVALID\n";

    // count total digit, and get reverse number
    int count_digit = 0;
    long number = c;
    long reverse = 0;
    while (number > 0)
    {
        long rest = number % 10;
        number = number - rest;
        number = number / 10;

        reverse = 10 * reverse + rest;
        count_digit = count_digit + 1;
    }

    // 34 = first 2 or digit = 37 AMEX len 15
    // 51 <= first 2 digit <= 55 MASTERCARD len 16
    // 4 == first digit VISA 13 <= len <= 16

    // check first digit and len of digit
    if ((count_digit == 13 || count_digit == 16) && reverse % 10 == 4)
    {
        result = "VISA\n";
    }
    else if (count_digit == 15)
    {
        long first = reverse % 10;
        long second = ((reverse - first) / 10) % 10;
        if (first == 3 && (second == 4 || second == 7))
        {
            result = "AMEX\n";
        }
        else
        {
            return "INVALID\n";
        }
    }
    else if (count_digit == 16)
    {
        long first = reverse % 10;
        long second = ((reverse - first) / 10) % 10;
        if (first == 5 & second >= 1 & second <= 5)
        {
            result = "MASTERCARD\n";
        }
        else
        {
            return "INVALID\n";
        }
    }
    else
    {
        return "INVALID\n";
    }

    // check Luhns algorimts conditions
    number = reverse;
    int i = count_digit % 2; // 0
    long sum_par = 0;
    long sum_impar = 0;
    while (number > 0)
    {
        long rest = number % 10;
        number = number - rest;
        number = number / 10;

        if (i % 2 == 0)
        {
            long multi = rest * 2;
            long val = multi % 10;
            if (multi >= 10)
            {
                val = val + 1;
            }

            sum_par = sum_par + val;
        }
        else
        {
            sum_impar = sum_impar + rest;
        }

        i = i + 1;
    }

    if ((sum_par + sum_impar) % 10 == 0)
    {
        return result;
    }
    else
    {
        return "INVALID\n";
    }
}

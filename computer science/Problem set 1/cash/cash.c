#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // 25 10 5 1
    // get cash valid
    int cash = 0;
    while (true)
    {
        cash = get_int("Change owed: ");
        if (cash >= 1)
        {
            break;
        }
    }

    int mount = 0;
    while (cash > 0)
    {
        if (cash >= 25)
        {
            cash = cash - 25;
            mount = mount + 1;
        }
        else if (cash >= 10)
        {
            cash = cash - 10;
            mount = mount + 1;
        }
        else if (cash >= 5)
        {
            cash = cash - 5;
            mount = mount + 1;
        }
        else
        {
            mount = mount + cash;
            cash = 0;
        }
    }
    printf("%i", mount);
}

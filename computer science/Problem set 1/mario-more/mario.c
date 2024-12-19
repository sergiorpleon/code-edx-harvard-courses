#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // get height valid
    int height = 0;
    while (true)
    {
        height = get_int("Height: ");
        if (height >= 1 & height <= 8)
        {
            break;
        }
    }

    // print blocks
    for (int i = 0; i < height; i++)
    {

        // print left row
        for (int j = 0; j < height; j++)
        {
            if (i + j < height - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }

        printf("  ");

        // print right row
        for (int j = 0; j < height; j++)
        {
            if (i + height - j < height)
            {
                // printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}

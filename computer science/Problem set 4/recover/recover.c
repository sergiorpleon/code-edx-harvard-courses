#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }
    // Open the memory card
    FILE *card = fopen(argv[1], "rb");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // While there's still data left to read from the memory card
    uint8_t buffer[512];

    int number = 0;
    char name[8];
    FILE *newimg = NULL;

    // read buffer
    while (fread(buffer, 1, 512, card) == 512)
    {
        // Create JPEGs from the data
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // close open file
            if (number != 0)
            {
                fclose(newimg);
                // printf("closed\n");
            }

            // open file
            sprintf(name, "%03i.jpg", number);
            // printf("%s\n", name);
            newimg = fopen(name, "wb");
            if (card == NULL)
            {
                printf("Could not open file.\n");
                return 1;
            }

            // increment image number
            number += 1;
        }

        // write buffer
        if (newimg != NULL)
        {
            fwrite(buffer, 1, 512, newimg);
            // printf(".");
        }
    }
    fclose(newimg);
    fclose(card);
    return 0;
}

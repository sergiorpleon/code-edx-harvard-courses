#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int isnumber(string text);
string encrypt(string text, int k);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Missing command-line arguments\n");
        return 1;
    }
    int k = isnumber(argv[1]);
    if (k != -1)
    {
        string plaintext = get_string("plaintext: ");
        string ciphertext = encrypt(plaintext, k);
        printf("ciphertext: %s\n", ciphertext);
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}

int isnumber(string text)
{
    int number = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((int) text[i] >= '0' & (int) text[i] <= '9')
        {
            number = number * 10 + (int) (text[i] - '0');
        }
        else
        {
            return -1;
        }
    }
    return number;
}

string encrypt(string text, int k)
{
    string newtext = text;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isupper(text[i]))
        {
            newtext[i] = (text[i] - 'A' + k) % 26 + 'A';
        }
        else if (islower(text[i]))
        {
            newtext[i] = (text[i] - 'a' + k) % 26 + 'a';
        }
    }
    return newtext;
}

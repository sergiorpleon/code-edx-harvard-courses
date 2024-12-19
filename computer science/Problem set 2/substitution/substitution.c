#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool isvalid(string text);
string encrypt(string text, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Missing command-line arguments\n");
        return 1;
    }

    if (isvalid(argv[1]))
    {
        string plaintext = get_string("plaintext: ");
        string ciphertext = encrypt(plaintext, argv[1]);
        printf("ciphertext: %s\n", ciphertext);
    }
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
}

bool isvalid(string text)
{
    if (strlen(text) != 26)
    {
        return false;
    }
    int number = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (tolower(text[i]) >= 'a' && tolower(text[i]) <= 'z')
        {
            for (int j = i + 1; j < strlen(text); j++)
            {
                if (text[i] == text[j])
                {
                    return false;
                }
            }
        }
        else
        {
            return false;
        }
    }
    return true;
}

string encrypt(string text, string key)
{
    string newtext = text;
    for (int i = 0; i < strlen(text); i++)
    {
        if (tolower(text[i]) >= 'a' && tolower(text[i]) <= 'z')
        {
            if (isupper(text[i]))
            {
                newtext[i] = key[text[i] - 'A'];
                if (islower(newtext[i]))
                {
                    newtext[i] = newtext[i] + ('A' - 'a');
                }
            }
            else if (islower(text[i]))
            {
                newtext[i] = tolower(key[text[i] - 'a']);
            }
        }
        else
        {
            newtext[i] = text[i];
        }
    }
    return newtext;
}

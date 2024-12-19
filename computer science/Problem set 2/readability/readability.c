#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");
    // Count the number of letters, words, and sentences in the text
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Compute the Coleman-Liau index
    float L = (float) letters / (float) words * 100;
    float S = (float) sentences / (float) words * 100;
    float index = round(0.0588 * L - 0.296 * S - 15.8);

    // Print the grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }else if (index == 1)
    {
        printf("Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) index);
    }
}

int count_letters(string text)
{
    // Return the number of letters in text
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (tolower(text[i]) >= 'a' & tolower(text[i]) <= 'z')
        {
            count += 1;
        }
    }
    return count;
}

int count_words(string text)
{
    // Return the number of words in text
    int count = 1;
    bool is_space = false;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            if (!is_space)
            {
                count += 1;
            }
            is_space = true;
        }
        else
        {
            is_space = false;
        }
    }
    return count;
}
int count_sentences(string text)
{
    // Return the number of sentences in text
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' | text[i] == '!' | text[i] == '?')
        {
            count += 1;
        }
    }
    return count;
}

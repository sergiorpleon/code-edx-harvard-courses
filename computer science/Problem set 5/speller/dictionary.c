// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool add(const char *word)
{
    // Add node with word to the hash table
    node *tmp = malloc(sizeof(node));
    tmp->next = NULL;
    sprintf(tmp->word, "%s", word);

    // insert tmp node
    if (table[hash(word)] == NULL)
    {
        table[hash(word)] = tmp;
    }
    else
    {
        tmp->next = table[hash(word)];
        table[hash(word)] = tmp;
    }
    return true;
}

void print()
{
    // print dictionary
    for (int i = 0; i < 26; i++)
    {
        if (table[i] != NULL)
        {
            // printf("%i", i);
            printf("%s", table[i]->word);
            node *next = table[i]->next;
            while (next != NULL)
            {
                printf("-%s", next->word);
                next = next->next;
            }
            printf("\n");
        }
    }
}

/// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    node *tmp = table[hash(word)];
    while (tmp != NULL)
    {
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }
        else
        {
            tmp = tmp->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // My hash function: Add and subtract the value of the consonants.
    // Find the module 26 and if it is negative add 26
    // Example: twitter = (t - w + t - t + r)%26 and sum 26 if mod is negative

    int index = 0;
    int direction = 1;
    double count = 0;
    while (word[index])
    {
        if (toupper(word[index]) != 'A' && toupper(word[index]) != 'E' &&
            toupper(word[index]) != 'I' && toupper(word[index]) != 'O' &&
            toupper(word[index]) != 'U' && word[index] != '\'')
        {
            count += (toupper(word[index]) - 'A') * direction;
            direction = direction * (-1);
        }
        index += 1;
    }
    int result = ((int) count % 26);
    if (result < 0)
    {
        result += 26;
    }
    return result;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return false;
    }

    for (int i = 0; i < 26; i++)
    {
        table[i] = NULL;
    }

    char c;
    char word[LENGTH + 1];
    sprintf(word, "");

    bool islastletter = false;
    while (fread(&c, sizeof(char), 1, file))
    {

        // Read each word in the file
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '\'')
        {
            if ((c >= 'A' && c <= 'Z'))
            {
                sprintf(word, "%s%c", word, c - ('A' - 'a'));
            }
            else
            {
                sprintf(word, "%s%c", word, c);
            }
            islastletter = true;
        }
        else
        {
            if (islastletter)
            {
                // printf("%s/", word);

                // Add each word to the hash table if not exist
                if (!check(word))
                {
                    add(word);
                }
                sprintf(word, "");
            }
            islastletter = false;
        }
    }
    if (islastletter)
    {
        // printf("%s", word);
        //  Add each word to the hash table
        if (!check(word))
        {
            add(word);
        }
    }
    sprintf(word, "");
    // printf("\n\n");

    fclose(file);

    // print();

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size()
{
    // TODO
    int count = 0;
    for (int i = 0; i < 26; i++)
    {
        if (table[i] != NULL)
        {
            // printf("%i", i);
            // printf("%s", table[i]->word);
            count += 1;
            node *next = table[i]->next;
            while (next != NULL)
            {
                // printf("-%s", next->word);
                count += 1;
                next = next->next;
            }
            // printf("\n");
        }
    }
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload()
{
    // TODO
    for (int i = 0; i < 26; i++)
    {
        if (table[i] != NULL)
        {
            // printf("%i", i);
            // printf("%s", table[i]->word);
            node *next = table[i]->next;
            table[i]->next = NULL;
            while (next != NULL)
            {
                // printf("-%s", next->word);
                node *tmp = next;

                next = next->next;

                tmp->next = NULL;
                free(tmp);
            }
            free(next);

            // printf("\n");
        }
    }

    // print();

    for (int i = 0; i < 26; i++)
    {
        if (table[i] != NULL)
        {
            node *next = table[i];
            table[i] = NULL;
            free(next);
        }
    }

    // print();
    return true;
}

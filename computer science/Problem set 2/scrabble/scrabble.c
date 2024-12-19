#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int score(string word);

int main(void)
{
    // Prompt the user for two words
    string player1 = get_string("Player 1: ");
    string player2 = get_string("Player 2: ");

    // Compute the score of each word
    int score_p1 = score(player1);
    int score_p2 = score(player2);

    // Print the winner
    if (score_p1 > score_p2)
    {
        printf("Player 1 wins!");
    }
    else if (score_p1 < score_p2)
    {
        printf("Player 2 wins!");
    }
    else
    {
        printf("Tie!");
    }
}

int score(string word)
{
    int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

    int total = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        int index = tolower(word[i]) - 'a';
        if (index >= 0 & index < 26)
        {
            total = total + points[index];
        }
    }
    return total;
}

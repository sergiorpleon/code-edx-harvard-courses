#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

bool check_patch(int a, int z, int count);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        printf("%i", ranks[i]);
    }
    printf("\n");
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (i < j)
            {
                preferences[ranks[i]][ranks[j]] += 1;
            }
        }
    }

    // print preference
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            printf("%i ", preferences[i][j]);
        }
        printf("\n");
    }

    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    pair_count = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pair thepair;
                thepair.winner = i;
                thepair.loser = j;
                pairs[pair_count] = thepair;
                pair_count += 1;
            }
            else if (preferences[j][i] > preferences[i][j])
            {
                pair thepair;
                thepair.winner = j;
                thepair.loser = i;
                pairs[pair_count] = thepair;
                pair_count += 1;
            }
        }
    }

    // print pairs
    for (int i = 0; i < pair_count; i++)
    {

        printf("%i/%i", pairs[i].winner, pairs[i].loser);
        printf("\n");
    }

    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    int index = 0;
    for (int i = 0; i < pair_count; i++)
    {
        for (int j = 1; j < pair_count - i; j++)
        {
            int preferi = preferences[pairs[j - 1].winner][pairs[j - 1].loser];
            int preferj = preferences[pairs[j].winner][pairs[j].loser];
            if (preferi < preferj)
            {
                int tmp_winner = pairs[j - 1].winner;
                int tmp_loser = pairs[j - 1].loser;

                pairs[j - 1].winner = pairs[j].winner;
                pairs[j - 1].loser = pairs[j].loser;

                pairs[j].winner = tmp_winner;
                pairs[j].loser = tmp_loser;
            }
        }
    }

    // print sort
    for (int i = 0; i < pair_count; i++)
    {
        printf("%i-%i", pairs[i].winner, pairs[i].loser);
        printf("\n");
    }

    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i = 0; i < pair_count; i++)
    {
        locked[pairs[i].winner][pairs[i].loser] = true;

        // check not loop
        if (check_patch(pairs[i].loser, pairs[i].winner, candidate_count))
        {
            locked[pairs[i].winner][pairs[i].loser] = false;
        }
    }

    // print locked
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[i][j])
            {
                printf("*");
            }
            else
            {
                printf("-");
            }
        }
        printf("\n");
    }
    return;
}

bool check_patch(int a, int z, int count)
{
    if (a == z)
    {
        return true;
    }
    if (count < 0)
    {
        return false;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[a][i])
        {
            if (check_patch(i, z, count - 1))
            {
                return true;
            }
        }
    }
    return false;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        bool iswinner = true;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                iswinner = false;
                break;
            }
        }
        if (iswinner)
        {
            printf("%s\n", candidates[i]);
            break;
        }
    }
    return;
}

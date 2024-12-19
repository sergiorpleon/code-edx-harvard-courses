import sys
import csv


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    if len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")
    if sys.argv[1].endswith(".csv") and sys.argv[2].endswith(".txt"):
        pass
    else:
        sys.exit("No valid arguments file")

    # TODO: Read database file into a variable
    sequence = ""
    with open(sys.argv[2]) as file:
        sequence = file.read()

    # TODO: Read DNA sequence file into a variable
    strs = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        strs = reader.fieldnames

    rows = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    # TODO: Find longest match of each STR in DNA sequence
    search = {}
    for str in strs[1:]:
        search[str] = longest_match(sequence, str)

    # TODO: Check database for matching profiles
    name = ""
    for row in rows:
        # math = True
        # for e in search:
        #    if not (int(search[e])==int(row[e])):
        #        math = False
        #        break

        if all(int(search[e]) == int(row[e]) for e in search):
            name = row["name"]

    if name == "":
        print("No match")
    else:
        print(name)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()

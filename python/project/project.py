import sys
import re
import random
import csv

import cryptocode

def main():
    case = valid_arg(sys.argv)

    #generate
    if case == 1 or case == 2:
        try:
            #case 2 render maze with emoji
            render_emoji = True if case==2 else False

            #create empty maze
            map = empty_map()
            print_map(map, render_emoji)

            #Enter route for maze and validate route
            path = input("Path: ")
            is_valid, map_path = validate_path(map, path)

            if is_valid:
                #Randomly insert random blocks, none on the path
                map = generate_map(map_path)
                print()
                print("Generate and salved map...")

                #Save the maze to file
                map_name=f"{sys.argv[2]}.txt"
                save_map(map_name, map, path)
                print_map(map, render_emoji)

            else:
                print("Incorrect path format or path does not reach the end")
        except ValueError:
            sys.exit("Value Error")

    #play
    elif case == 3 or case == 4:
        try:
            #case 4 render maze with emoji
            render_emoji = True if case==4 else False

            #Load file maze
            map_name=f"{sys.argv[2]}.txt"
            map, path = load_map(map_name)
            print_map(map, render_emoji)
            #print(path)

            #Validate map and path
            if not validate_map(map):
                sys.exit("Invalid maze")

            if not validate_path(map, path):
                sys.exit("Invalid path")

            #User has three attempts to find a way to solve the maze
            intent = 3
            while intent!=0:
                path = input("Path: ")

                #If I validate I read the scores file and update it if required.
                is_valid, new_map = validate_path(map, path)
                if is_valid:
                    print("=MAZE SOLVED=")
                    person = input("Your Name: ")

                    score_name=f"score_{sys.argv[2]}.csv"
                    scores = read_score(score_name)

                    #requires saving if person has no score or improves existing score
                    need_save, update_scores = update_score(person, score_name, scores, path)
                    if need_save:
                        save_score(score_name, update_scores)

                    print(f"Congratulation {person}!!!")
                    break
                else:
                    pass
                intent = intent - 1

            if intent == 0:
                print("=MAZE NOT SOLVED=")
                print("Maximum number of attempts made")
        except FileNotFoundError:
            sys.exit("File not found")
        except TypeError:
            sys.exit("Corrupted file")
    elif case == 5 or case == 6:
        try:
            render_emoji = True if case==6 else False

            #load map
            map_name=f"{sys.argv[2]}.txt"
            map, path = load_map(map_name)
            path=sys.argv[3]

            if not validate_map(map):
                sys.exit("Invalid maze")

            print_map(map, render_emoji)

            if not validate_path(map, path):
                print("Route does not solve maze")
                sys.exit("Invalid path")

            else:
                print("Valid maze. Saved...")

            save_map(map_name, map, path)
        except FileNotFoundError:
            sys.exit("File not found")
        except TypeError:
            sys.exit("Corrupted file")
    elif case == 7:
        try:
            score_name=f"score_{sys.argv[2]}.csv"
            print(f"===============")
            print(f"| Steps | Person")
            print(f"===============")
            with open(score_name) as file:
                reader = csv.DictReader(file, fieldnames=["key","person", "step"])
                for row in reader:
                    message =  decrypt(score_name, row["key"])
                    if f"{row["person"]}{row["step"]}" == message:
                        print(f"|  {int(row["step"]):03}  | {row["person"]}")
                    else:
                        print("Corrupted score")
            #print_score(score_name)
        except FileNotFoundError:
            sys.exit("File dont exist")
        #except ValueError:
        #    sys.exit("Value error")
    elif case == 8:
        print("Commands:")
        print("python project.py -g map_name [-e] OR python project.py --generate map_name [--emoji]")
        print("With the command you pass the name of the map as a parameter. You are asked to enter a path that goes from the x or the crab to the mas or castle.")
        print("The path must be generated having the following criteria; first letter of movement direction (R of Right, L of Left, U of Up or D of Down) followed by a number from 1-9 that will indicate the number of steps to take.")
        print("Example of a path: R4D4L2D2R5D3R2")
        print("")
        print("python project.py -p map_name [-e] OR python project.py --play map_name [--emoji]")
        print("With the command you pass the name of the maze you want to play as a parameter. You are then asked to enter a path that goes from the x or crab to the plus or castle. You have three attempts to solve the maze.")
        print("The path must be generated having the following criteria; first letter of movement direction (R of Right, L of Left, U of Up or D of Down) followed by a number from 1-9 that will indicate the number of steps to take.")
        print("Your best result will be saved in a score file.")
        print("")
        print("python project.py -c map_name solution_path [-e] OR python project.py --create map_name solution_path [--emoji]")
        print("You can open the .txt file of the maze and change the start and end points of the map blocks. You can also add two blocks ([B] and [F]) to create more interesting maps.")
        print("Once you have made changes to the map file, you can run this command to save the maze for use.")
        print("With the command you pass the name of the map and the solution and it validates if the maze is correct. If the maze and path are corrects it saves the maze and the encrypted solution.")
        print("The solution must be generated using the following criteria; enter the first letter of the direction of movement (R of Right, L of Left, U of Up or D of Down) followed by a number from 1-9 that indicates the number of steps to take.")
        print("")
        print("python project.py -s map_name OR python project.py --score map_name")
        print("Displays the scores of a maze.")
        print("")
        print("The optional parameter -e or --emoji. Use emoji to render the map prettier in console.")
        print("[|] and [-]: borders")
        print("[x]: Starting point.")
        print("[+]: Goal.")
        print("[ ]: Free space.")
        print("[*]: barrier.")
        print("[B]: Movable block, can be pushed as long as the direction you push it has space for the block to move.")
        print("[F]: Indicates fruits that you must collect. If you reach the goals without collecting all the fruit, the maze will not be solved.")
        print("")
        print("Enjoy solving, creating and sharing mazes with friends.")
        sys.exit()
    else:
        print("See help with: python project.py --help")
        sys.exit("Invalid arguments")

def valid_arg(argv):
    #number of incorrect arguments
    if len(sys.argv)<2:
        return -1
    if len(sys.argv)>5:
        return -1

    #generate command check
    if len(argv) == 3 and (argv[1]=="-g" or argv[1]=="--generate") and argv[2].isalnum():
        return 1
    elif len(argv) == 4 and (argv[1]=="-g" or argv[1]=="--generate") and argv[2].isalnum() and (argv[3]=="-e" or argv[3]=="--emoji"):
        return 2

    #play command check
    elif len(argv) == 3 and (argv[1]=="-p" or argv[1]=="--play") and argv[2].isalnum():
        return 3
    elif len(argv) == 4 and (argv[1]=="-p" or argv[1]=="--play") and argv[2].isalnum() and (argv[3]=="-e" or argv[3]=="--emoji"):
        return 4

    #create command check
    elif len(argv) == 4 and (argv[1]=="-c" or argv[1]=="--create") and argv[2].isalnum() and argv[3].isalnum():
        return 5
    elif len(argv) == 5 and (argv[1]=="-c" or argv[1]=="--create") and argv[2].isalnum() and argv[3].isalnum() and (argv[4]=="-e" or argv[4]=="--emoji"):
        return 6

    #score command check
    elif len(argv) == 3 and (argv[1]=="-s" or argv[1]=="--score") and argv[2].isalnum():
        return 7
    #help command check
    elif len(argv) == 2 and (argv[1]=="-h" or argv[1]=="--help"):
        return 8
    else:
        return -1

def empty_map():
    #Generating empty maze with edges and start and end points
    map = []
    for i in range(12):
        row = []
        for j in range(12):
            if i == 0 or i == 11:
                row.append("[-]")
            elif j == 0 or j == 11:
                row.append("[|]")
            else:
                row.append("[ ]")
        map.append(row)
    map[1][1] = "[X]"
    map[10][10] = "[+]"
    return map

def print_map(map, pretty=False):
    #Printing map with emoji or characters, as appropriate
    for row in map:
        str_row = ""
        for cell in row:
            if pretty:
                #print emoji segun elemento
                if cell == "[|]" or cell == "[-]" or cell == "[*]":
                    print("🟥", end='')
                elif cell in ["[R]","[L]","[U]","[D]","[r]","[l]","[u]","[d]"]:
                    print("⚪", end='')
                elif cell == "[ ]":
                    print("⬛", end='')
                elif cell == "[+]":
                    print("🏰", end='')
                elif cell == "[x]" or cell == "[X]":
                    print("🦀", end='')
                elif cell == "[B]":
                    print("🎲", end='')
                elif cell == "[F]":
                    print("🍎", end='')
            else:
                #confirmi fila de caracteres
                str_row = str_row + f"{cell}"
        if pretty:
            print("")
        else:
            print(str_row)


def generate_map(map_path):
    #generate random block outside of path
    number = random.randrange(50, 70)
    for n in range(number):
        pos_x = random.randrange(1, 11)
        pos_y = random.randrange(1, 11)
        if map_path[pos_x][pos_y] == "[ ]":
            map_path[pos_x][pos_y] = "[*]"

    #Setting the path as an empty cell
    for i in range(11):
        for j in range(11):
            if map_path[i][j] in ["[r]","[l]","[u]","[d]","[R]","[L]","[U]","[D]"]:
                map_path[i][j] = "[ ]"

    return map_path

def save_map(map_name, map, path):
    #Save maze
    with open(map_name, 'w') as file:
        for i in range(12):
            row = ""
            for j in range(12):
                row = row + map[i][j]
            file.write(f"{row}\n")
        file.write(encrypt(map_name, path))


def load_map(map_name):
    #Load map
    try:
        with open(map_name, "r", newline="\n") as file:
            map = []
            i = 0
            encoded = ""
            for line in file:
                row = []
                for cell in line.strip():
                    if cell!="[" and cell!="]":
                        row.append(f"[{cell}]")
                if i == 12:
                    encoded = line
                else:
                    map.append(row)
                i = i + 1
        path = decrypt(map_name, encoded)
        return map, path

    except FileNotFoundError:
        raise FileNotFoundError

def update_score(person, score_name, scores, path):
    #Count the steps of the solution
    count = 0
    for p in path:
        try:
            step = int(p)
            count = count + step
        except ValueError:
            pass

    key = encrypt(score_name, f"{person}{count}")
    myscore = {"key":key, "person":person, "step": f"{count}"}

    #if person exist and score is better, update value
    need_save = False
    have_score = False
    for s in sorted(scores, key = lambda scores: scores["step"]):
        if s["person"]==myscore["person"] and s["step"]>myscore["step"]:
            s["step"] = myscore["step"]
            need_save = True
            have_score = True
        elif s["person"]==myscore["person"]:
            have_score = True

    #if person not exist, add person with setps of solution to scores
    if need_save == False and have_score==False:
        if len(scores) > 10:
            scores.pop()
        scores.append(myscore)
        need_save = True

    return need_save, scores

def read_score(score_name):
    #read score file
    scores=[]
    try:
        with open(score_name) as file:
            reader = csv.DictReader(file, fieldnames=["key", "person", "step"])
            for row in reader:
                message = decrypt(score_name, row["key"])
                if message == f"{row["person"]}{row["step"]}":
                    score = {"key":row["key"], "person":row["person"], "step": row["step"]}
                else:
                    return []
                scores.append(score)
    except FileNotFoundError:
        return []
    except ValueError:
        return []
    return scores

def save_score(score_name, scores):
    #save score
    with open(score_name, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["key", "person", "step"])
        for s in sorted(scores, key = lambda scores: scores["step"]):
            writer.writerow(s)

def validate_path(map, path):
    try:
        matches = re.search(r"^(([RrLlUuDd]{1}[1-9]{1})+)$", path)
        map_path = []
        if matches:
            #Replicate map to check path
            for row in map:
                row_path = []
                for cell in row:
                    row_path.append(cell)

                map_path.append(row_path)

            #Count the fruits
            count_fruit = 0
            for row in map_path:
                for cell in row:
                    if cell == "[F]":
                        count_fruit = count_fruit + 1

            #Check that the solution collects all the fruits and reaches the end
            pos_x = 1
            pos_y = 1
            dir = ""
            for cell in path:
                if dir=="":
                    dir = cell
                else:
                    step = int(cell)
                    dir_x = 0
                    dir_y = 0
                    for s in range(step):
                        if dir.lower() == "r":
                            dir_x = int(1)
                            dir_y = int(0)
                        if dir.lower() == "l":
                            dir_x = int(-1)
                            dir_y = int(0)
                        if dir.lower() == "d":
                            dir_x = int(0)
                            dir_y = int(1)
                        if dir.lower() == "u":
                            dir_x = int(0)
                            dir_y = int(-1)


                        if map_path[pos_y+dir_y][pos_x+dir_x] in ["[ ]","[R]","[L]","[U]","[D]","[r]","[l]","[u]","[d]"]:
                            #If there is empty space or already covered, I move
                            pos_x = pos_x+dir_x
                            pos_y = pos_y+dir_y
                            map_path[pos_y][pos_x] = f"[{dir}]"
                        elif map_path[pos_y+dir_y][pos_x+dir_x] == "[B]" and map_path[pos_y+dir_y+dir_y][pos_x+dir_x+dir_x] == "[ ]":
                            #If place with block I move block whenever next space is empty
                            pos_x = pos_x+dir_x
                            pos_y = pos_y+dir_y
                            map_path[pos_y][pos_x] = f"[{dir}]"
                            map_path[pos_y+dir_y][pos_x+dir_x] = "[B]"
                        elif map_path[pos_y+dir_y][pos_x+dir_x] == "[F]":
                            #If there is a place with fruit, I will subtract one quantity of fruit
                            pos_x = pos_x+dir_x
                            pos_y = pos_y+dir_y
                            map_path[pos_y][pos_x] = f"[{dir}]"
                            count_fruit = count_fruit - 1
                        elif map_path[pos_y+dir_y][pos_x+dir_x] == "[+]" and count_fruit == 0:
                            return True, map_path
                    dir = ""

            return False, map_path
        else:
            return False, map_path
    except IndexError:
        raise IndexError
    except ValueError:
        raise ValueError
    except TypeError:
        raise TypeError

def validate_map(map):
    count_x = 0
    count_plus = 0
    if len(map) != 12:
        return False
    for row in map:
        if len(row) != 12:
            return False

        for cell in row:
            #Validate blocks of those defined
            values = ["[r]","[R]","[l]","[L]","[u]","[U]","[d]","[D]","[ ]","[*]","[x]","[X]","[+]","[|]","[-]","[F]","[B]"]
            if not cell in values:
                return False
            else:
                #Check if there is more than one start and more than one end
                if cell == "[X]"or cell == "[x]":
                    count_x = count_x + 1
                if cell == "[+]":
                    count_plus = count_plus + 1
                if count_x > 1 or count_plus > 1:
                    return False

    return True

def encrypt(key, message):
    encoded = cryptocode.encrypt(message,key)
    return encoded

def decrypt(key, message):
    decoded = cryptocode.decrypt(message,key)
    return decoded


if __name__ == "__main__":
    main()

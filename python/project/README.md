# MAZE
#### Video Demo:  <https://youtu.be/VWlSrJfRAs8>
#### Description:
The project allows you to generate maze with the route you define, solve a maze, modify a maze to make it your own. It will also save the score and allow you to view it. Get inspired and create incredible mazes and challenge friends to solve them.

The project allows you to generate 10 by 10 maps, entering the route that the player must take to solve the maze.
The project saves the generated map in a .txt file with the path encrypted to prevent new players. For that the cryptocode library is used (pip install cryptocode)
The paths that the player enters must have an initial letter that indicates the direction of movement (R for Right, L for Right, U for Right, D for Right), followed by a one-digit number that indicates how many steps the player must move in. that address.
The project allows you to solve a maze, the player will have three attempts
The project saves the player's score in a .csv. The score is saved as an element before an encrypted key that will allow detecting if the user alters the score by modifying the .csv
The project allows the user to create their own map from a generated map. You can change the start and end square of the maze, create the walls as you wish, as well as incorporate new types of squares already defined.
The project allows you to view the score on the console.
The project allows you to visualize a maze using letters or using emoji. Using emoji is more understandable for the player.

#### The project has the functions:
-valid_arg(argv): Validates that the arguments are correct
-vacio_map(): Generates an empty map with only borders, and a start and end box
-print_map(map, Pretty=False): Print maze in console using lettersor using emoji
-generate_map(map_path): From an empty map with the route, generate blocks randomly on the map. Never place them on the solution route of the map
-save_map(map_name, map, route): save a map to a .txt file
-load_map(map_name): load map
-update_score(person, score_name, scores, path): Updates scores with the player's new score
-read_score(score_name): read score from file.csv
-save_score(score_name, scores): save score to .csv file
-validate_route(map, route): validate route
-validate_map(map): validate map
-encrypt(key, message): encrypt message
-decrypt(key, message): decrypt message

#### Testing
It has a test file, which has four test functions that check different conditions within.

test_valid_arg
-Few arguments
-Many arguments
-Incorrect parameters, not -g -p -c -s
-Incorrect parameters, not digittext
-Correctly formatted parameters

validate_map
-Maze dimension incorrect
-Default empty maze
-Incorrect, two begin
-Incorrect, two end
-Incorrect, block does not exist

validate_path
-Route correct
-Route not correct
-Route with doble digit
-Route not finish
-Route, check no problem with walls
-Check block type Fruit
-Check can move block
-Check can not move block
-Check block type Fruit
-Ending up leaving without picking one fruit
-Finishing by collecting the fruit
-Ending up leaving without picking two fruits
-Finishing by collecting the two fruits

update_score
-No need to save person, score is the same
-Does not require saving the person with the highest score
-Requires saving person with lower score
-Requires saving new person


#### Commands
python project.py -g map_name [-e] OR python project.py --generate map_name [--emoji]

With the command you pass the name of the map as a parameter. You are asked to enter a path that goes from the x or the crab to the mas or castle.
The path must be generated having the following criteria; first letter of movement direction (R of Right, L of Left, U of Up or D of Down) followed by a number from 1-9 that will indicate the number of steps to take.
Example of a path: R4D4L2D2R5D3R2


python project.py -p map_name [-e] OR python project.py --play map_name [--emoji]

With the command you pass the name of the maze you want to play as a parameter. You are then asked to enter a path that goes from the x or crab to the plus or castle. You have three attempts to solve the maze.
The path must be generated having the following criteria; first letter of movement direction (R of Right, L of Left, U of Up or D of Down) followed by a number from 1-9 that will indicate the number of steps to take.
Your best result will be saved in a score file.


python project.py -c map_name solution_path [-e] OR python project.py --create map_name solution_path [--emoji]")

You can open the .txt file of the maze and change the start and end points of the map blocks. You can also add two blocks ([B] and [F]) to create more interesting maps.
Once you have made changes to the map file, you can run this command to save the maze for use.")
With the command you pass the name of the map and the solution and it validates if the maze is correct. If the maze and path are corrects it saves the maze and the encrypted solution.
The solution must be generated using the following criteria; enter the first letter of the direction of movement (R of Right, L of Left, U of Up or D of Down) followed by a number from 1-9 that indicates the number of steps to take.


python project.py -s map_name OR python project.py --score map_name

Displays the scores of a maze.

The optional parameter -e or --emoji. Use emoji to render the map prettier in console.

#### BLocks:
[|] and [-]: borders
[x]: Starting point.
[+]: Goal.
[ ]: Free space.
[*]: barrier.
[B]: Movable block, can be pushed as long as the direction you push it has space for the block to move.
[F]: Indicates fruits that you must collect. If you reach the goals without collecting all the fruit, the maze will not be solved.

Enjoy solving, creating and sharing mazes with friends.

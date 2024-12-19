import pytest
from project import valid_arg, validate_map, validate_path, empty_map, update_score


def test_valid_arg():
    #Few arguments
    assert valid_arg(["project.py"])==-1
    #Many arguments
    assert valid_arg(["project.py", "-c", "demo", "R9D9", "-e", "more"])==-1
    #Incorrect parameters, not -g -p -c -s
    assert valid_arg(["project.py", "-a", "demo"])==-1
    #Incorrect parameters, not digittext
    assert valid_arg(["project.py", "-g", "demo.."])==-1
    #Correctly formatted parameters
    assert valid_arg(["project.py", "-g", "demo"])==1
    assert valid_arg(["project.py", "-g", "demo", "-e"])==2
    assert valid_arg(["project.py", "-g", "demo", "--emoji"])==2
    assert valid_arg(["project.py", "--generate", "demo"])==1
    assert valid_arg(["project.py", "--generate", "demo", "--emoji"])==2
    assert valid_arg(["project.py", "-p", "demo"])==3
    assert valid_arg(["project.py", "-p", "demo", "-e"])==4
    assert valid_arg(["project.py", "--play", "demo"])==3
    assert valid_arg(["project.py", "--play", "demo", "--emoji"])==4
    assert valid_arg(["project.py", "-c", "demo", "R9D9"])==5
    assert valid_arg(["project.py", "-c", "demo", "R9D9", "-e"])==6
    assert valid_arg(["project.py", "--create", "demo", "R9D9"])==5
    assert valid_arg(["project.py", "--create", "demo", "R9D9", "--emoji"])==6
    assert valid_arg(["project.py", "-s", "demo"])==7
    assert valid_arg(["project.py", "--score", "demo"])==7
    assert valid_arg(["project.py", "-h"])==8
    assert valid_arg(["project.py", "--help"])==8



def test_validate_map():
    #Maze dimension incorrect
    assert validate_map([])==False
    assert validate_map([[" ", " "],[" ", " "]])==False
    #Default empty maze
    map = empty_map()
    assert validate_map(map)
    #Incorrect, two begin
    val = map[5][5]
    map[5][5]="[x]"
    assert validate_map(map)==False
    #Incorrect, two end
    map[5][5]="[+]"
    assert validate_map(map)==False
    #Incorrect, block does not exist
    map[5][5]="[@]"
    assert validate_map(map)==False


def test_validate_path():
    map = empty_map()
    #Route correct
    assert validate_path(map, "R9D9")[0]==True
    assert validate_path(map, "R9L4R4D5U1D5")[0]==True
    #Route not correct
    assert validate_path(map, "R9F9")[0]==False
    assert validate_path(map, "RR8F9")[0]==False
    #Route with doble digit
    assert validate_path(map, "R98F9")[0]==False
    assert validate_path(map, "R10F9")[0]==False
    #Route not finish
    assert validate_path(map, "R9D5")[0]==False

    #Route, check no problem with walls
    assert validate_path(map, "R5R6F9")[0]==False

    #Check block type Fruit
    map[2][7] = "[B]"
    #Check can move block
    assert validate_path(map, "R6D3U3R3D9")[0]==True
    #Check can not move block
    map[2][8] = "[B]"
    map[3][8] = "[*]"
    assert validate_path(map, "R7D3U3R2D9")[0]==True and map[2][8] == "[B]"


    #Check blovk type Fruit
    map[2][5] = "[F]"
    #Ending up leaving without picking one fruit
    assert validate_path(map, "R9D9")[0]==False
    #Finishing by collecting the fruit
    assert validate_path(map, "R4D1U1R5D9")[0]==True
    map[6][9] = "[F]"
    #Ending up leaving without picking two fruits
    assert validate_path(map, "R4D1U1R5D9")[0]==False
    #Finishing by collecting the two fruits
    assert validate_path(map, "R4D1U1R5D5L1R1D4")[0]==True


def test_update_score():
    scores = [ {"key":"QtOpCKwdyDrz*0390oBRlN1XzS10G8pnCKg==*HZQpAn1ADwTVf8mm9XMf7g==*CNqTty9esmFC8q30qN3anw==", "person":"People1","step":"18"},
{"key":"meIJMNfagKS9*t29W4NPnqEx8+xDVlE/4eQ==*/gBMmJbgn1o/TJUeDLzcbA==*VYJnARWY18gxlTjvGRSsKQ==","person":"People2","step":"18"},
{"key":"Ab9qAhY0EMZU*zfi/sY4VaVLuH4OzxgWXig==*XIy9Q0vFBpQDZMsdR/XIBQ==*8rpledhcmsyZmxsK3StDTg==","person":"People3","step":"18"}]
    #No need to save person, score is the same
    assert update_score("People1", "score_demo.csv", scores, "R9D9")[0] == False
    #Does not require saving the person with the highest score
    assert update_score("People1", "score_demo.csv", scores, "R6R5D9")[0] == False

    #Requires saving person with lower score
    u, s = update_score("People1", "score_demo.csv", scores, "R9D8")
    assert u == True and s[0]["step"] == "17"

    #Requires saving new person
    u, s = update_score("People4", "score_demo.csv", scores, "R9D9")
    assert u == True and s[3]["step"] == "18" and s[3]["person"] == "People4"


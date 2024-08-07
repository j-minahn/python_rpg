# Package to take in arrow key inputs
import copy
import os
from pynput import keyboard
from pynput.keyboard import Key
import time

# Define floor layouts and the player's starting location per floor
# This map will have three floors, which you can freely travel through until the player recahes
# the exit (represented as the letter E)

# Key to special tiles:
# U: Go upstairs
# D: Go downstairs
# P: Person that you can talk to (walk into them)
map = [
    ["▄▄▄▄▄▄▄▄▄▄▄▄",
     "█          █",
     "█ █ █ ██████",
     "█ █ █     U█",
     "█ █ ████████",
     "█O█       P█",
     "▀▀▀▀▀▀▀▀▀▀▀▀"],
    ["▄▄▄▄▄▄▄▄▄▄▄▄",
     "█      █   █",
     "████ █ █ █O█",
     "█U█P █   █D█",
     "█ █████ ████",
     "█          █",
     "▀▀▀▀▀▀▀▀▀▀▀▀"],
    ["▄▄▄▄▄▄▄▄▄▄▄▄",
     "█      █ P █",
     "███ █ ███ ██",
     "█D█ █      █",
     "█O█ █████ ██",
     "█     █E   █",
     "▀▀▀▀▀▀▀▀▀▀▀▀"]
]

# Define wall tiles
walls = ["▄", "▀", "█"]

# Define character that represents the player
player = "O"

# Player's starting coordinates for each floor
# Applies when going up from lower floor
floor_coords = ([0, 0], [9, 3], [0, 1])

# Player's starting coordinates when going down from higher floor
down_coords = ([8, 2], [0, 1], None)

# Different NPC dialogues depending on floor
dialogue = ["Welcome to the Mysterious Maze!",
            "You're halfway there! Are you tired yet?",
            "Not too far from the exit now!"]

# Boolean that represents whether the player is speaking to an NPC or not
speaking = False

# Current floor
floor = 1

# Map to load for current floor
current_map = map[0]

# Player's current coordinates for current floor
current_coords = [0, 0]

# Prints the current floor number and map
def printMap():
    print(f"{f"{floor}F":=^12}\n")
    print('\n'.join(current_map))

# Defines player and maze behavior when walking into a special tile
def event(tile):

    global floor
    global current_coords
    global current_map
    global speaking

    # os.system('cls')
    print('\033[10A\033[2K', end='')

    # Go up
    if tile == 'U':

        # Update the player's starting coordinates and map according to the new floor
        floor += 1
        floor_coords_copy = copy.deepcopy(floor_coords)
        current_coords = floor_coords_copy[floor - 1]
        current_map = map[floor - 1]

        # Print text indicating that the player is going up
        print(f"Now loading Floor {floor}")
        time.sleep(1)
        os.system('cls')
    
    # Go down
    elif tile == 'D':

        # Update the player's starting coordinates and map according to the new floor
        floor -= 1
        down_coords_copy = copy.deepcopy(down_coords)
        current_coords = down_coords_copy[floor - 1]
        current_map = map[floor - 1]

        # Print text indicating that the player is going down
        print(f"Now loading Floor {floor}")
        time.sleep(1)
        os.system('cls')
    
    # Talk to person
    elif tile == 'P':

        # Update player's speaking status to temporarily stop taking keyboard input
        speaking = True

        # Print out dialogue
        # Dialogue stays on screen until player inputs A
        choice = ""

        while choice != "A":
            print(dialogue[floor - 1])
            choice = input("Press A to continue: ")

        # Place player back to previous location and update speaking status so that
        # the player can move again
        os.system('cls')
        speaking = False
    
    # Reach goal
    elif tile == 'E':

        # Print the victory message, stop taking keyboard input and indicate that a special
        # event happened to prevent any more maze/player updates
        listener.stop()
        print("You win!")
        time.sleep(3)
        return True
    
    # No special tile reached
    else:

        # Indicate that nothing happened and that the player may move normally
        return False
    
    printMap()

    # Indicate that a special event happened to prevent maze/player updates
    return True

# Defines player and maze behavior when moving up or down
def upDown(direction):

    # Save the line that the player is currently in
    curr_line = current_map[-(current_coords[1] + 2)]

    # Get the line and tile that the player will be in if movement if successful
    if direction == "up":
        next_line = current_map[-(current_coords[1] + 3)]
        next_tile = current_map[-(current_coords[1] + 3)][current_coords[0] + 1]
    else:
        next_line = current_map[-(current_coords[1] + 1)]
        next_tile = current_map[-(current_coords[1] + 1)][current_coords[0] + 1]
    
    # Determine if the move is valid
    if next_line[current_coords[0] + 1] in walls:
        return "You bumped into a wall!"
    
    # Determine if the move will result in something special
    if event(next_tile):
        return

    # If move is valid, begin visually updating the maze
    # os.system('cls')
    print('\033[10A\033[2K', end='')
    updated_next_line = ""
    updated_prev_line = ""

    # Write the line that the player will be in
    # Write in the player for their future location
    for index, tile in enumerate(next_line):
        if index == current_coords[0] + 1:
            updated_next_line += player
        else:
            updated_next_line += tile

    # Write the line that the player will leave
    # Leave a blank space for the player's previous location
    for index, tile in enumerate(curr_line):
        if index == current_coords[0] + 1:
            updated_prev_line += ' '
        else:
            updated_prev_line += tile

    # Overwrite the appearance of the two lines and update the player's coordinates
    current_map[-(current_coords[1] + 2)] = updated_prev_line

    if direction == "up":
        current_map[-(current_coords[1] + 3)] = updated_next_line
        current_coords[1] += 1
    else:
        current_map[-(current_coords[1] + 1)] = updated_next_line
        current_coords[1] -= 1

    printMap()

    return

# Defines player and maze behavior when moving left or right
def leftRight(direction):

    # Save the line that the player is currently in
    curr_line = current_map[-(current_coords[1] + 2)]

    # Get the tile that the player will be in if movement if successful
    if direction == "left":
        next_tile = current_map[-(current_coords[1] + 2)][current_coords[0]]
    else:
        next_tile = current_map[-(current_coords[1] + 2)][current_coords[0] + 2]

    # Determine if the move is valid
    if (direction == "left" and curr_line[current_coords[0]] in walls) or (direction == "right" and curr_line[current_coords[0] + 2] in walls):
        return "You bumped into a wall!"

    # Determine if the move will result in something special
    if event(next_tile):
        return

    # If move is valid, begin visually updating the maze
    # os.system('cls')
    print('\033[10A\033[2K', end='')
    updated_next_line = ""

    # Write the line that the player will be in
    for index, tile in enumerate(curr_line):
        if (direction == "left" and index == current_coords[0]) or (direction == "right" and index == current_coords[0] + 2):
            updated_next_line += player
        elif index == current_coords[0] + 1:
            updated_next_line += ' '
        else:
            updated_next_line += tile

    # Overwrite the appearance of the line
    current_map[-(current_coords[1] + 2)] = updated_next_line

    # Update the player's coordinates
    if direction == "left":
        current_coords[0] -= 1
    else:
        current_coords[0] += 1
    
    printMap()

    return

# Moves the player, but only when not speaking to an NPC
def on_press(key):
    if key == Key.right and not speaking:
        leftRight("right")
    elif key == Key.left and not speaking:
        leftRight("left")
    elif key == Key.up and not speaking:
        upDown("up")
    elif key == Key.down and not speaking:
        upDown("down")
    elif key == Key.esc:
        listener.stop()

# Prints the start of the game and begins to take keyboard input
printMap()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
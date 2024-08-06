# Package to take in arrow key inputs
import os
from pynput import keyboard
from pynput.keyboard import Key

# Define map and starting location of player
map = [
    "▄▄▄▄▄▄▄▄▄▄▄▄",
    "█          █",
    "█ █ █ ██████",
    "█ █ █     E█",
    "█ █ ████████",
    "█O█        █",
    "▀▀▀▀▀▀▀▀▀▀▀▀"
]

# Define wall tiles
walls = ["▄", "▀", "█"]

# Player representation
player = "O"

# Player's starting coordinates
coords = [0, 0]

# Print entire map
print('\n'.join(map))

def upDown(direction):

    # Get the line that the player is currently in
    curr_line = map[-(coords[1] + 2)]

    # Get the line that the player will be in if movement if successful
    if direction == "up":
        next_line = map[-(coords[1] + 3)]
    else:
        next_line = map[-(coords[1] + 1)]
    
    # Determine if the move is valid
    if next_line[coords[0] + 1] in walls:
        return "You bumped into a wall!"

    # If move is valid, begin visually updating the maze
    os.system('cls')
    updated_next_line = ""
    updated_prev_line = ""

    # Write the line that the player will be in
    for index, tile in enumerate(next_line):
        if index == coords[0] + 1:
            updated_next_line += player
        else:
            updated_next_line += tile

    # Write the line that the player will leave
    for index, tile in enumerate(curr_line):
        if index == coords[0] + 1:
            updated_prev_line += ' '
        else:
            updated_prev_line += tile

    # Overwrite the appearance of the two lines and update the player's coordinates
    map[-(coords[1] + 2)] = updated_prev_line

    if direction == "up":
        map[-(coords[1] + 3)] = updated_next_line
        coords[1] += 1
    else:
        map[-(coords[1] + 1)] = updated_next_line
        coords[1] -= 1

    # Print the player's new location
    print('\n'.join(map))

    # Print victory message and stop taking keyboard inputs if the player reached the exit
    if next_line[coords[0] + 1] == 'E':
        print("You win!")
        listener.stop()

    return

def leftRight(direction):

    # Get the line that the player is currently in
    curr_line = map[-(coords[1] + 2)]
    
    # Determine if the move is valid
    if (direction == "left" and curr_line[coords[0]] in walls) or (direction == "right" and curr_line[coords[0] + 2] in walls):
        return "You bumped into a wall!"

    # If move is valid, begin visually updating the maze
    os.system('cls')
    updated_next_line = ""

    # Write the line that the player will be in
    for index, tile in enumerate(curr_line):
        if (direction == "left" and index == coords[0]) or (direction == "right" and index == coords[0] + 2):
            updated_next_line += player
        elif index == coords[0] + 1:
            updated_next_line += ' '
        else:
            updated_next_line += tile

    # Overwrite the appearance of the line
    map[-(coords[1] + 2)] = updated_next_line

    # Update the player's coordinates
    if direction == "left":
        coords[0] -= 1
    else:
        coords[0] += 1

    # Print the player's new location
    print('\n'.join(map))

    # Print victory message and stop taking keyboard inputs if the player reached the exit
    if curr_line[coords[0] + 1] == 'E':
        print("You win!")
        listener.stop()
    
    return

# Moves the player
def on_press(key):
    if key == Key.right:
        leftRight("right")
    elif key == Key.left:
        leftRight("left")
    elif key == Key.up:
        upDown("up")
    elif key == Key.down:
        upDown("down")
    elif key == Key.esc:
        listener.stop()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
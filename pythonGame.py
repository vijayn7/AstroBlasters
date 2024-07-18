import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Python-Game")

# Set up the canvas
canvas_width = 400
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Create Player
player_size = 30
player_x = canvas_width // 2
player_y = canvas_height // 2
player = canvas.create_rectangle(
    player_x - player_size // 2, 
    player_y - player_size // 2, 
    player_x + player_size // 2, 
    player_y + player_size // 2, 
    fill="blue"
)

# Movement state
move_directions = {'w': False, 's': False, 'a': False, 'd': False}

# Move the player in the current direction
def move_player():
    x, y = 0, 0
    if move_directions['w']:
        y = -5
    if move_directions['s']:
        y = 5
    if move_directions['a']:
        x = -5
    if move_directions['d']:
        x = 5

    # Get the current position of the player
    player_coords = canvas.coords(player)

    # Check for canvas boundaries
    if player_coords[0] + x < 0:
        x = -player_coords[0]  # Prevent moving left off the canvas
    if player_coords[1] + y < 0:
        y = -player_coords[1]  # Prevent moving up off the canvas
    if player_coords[2] + x > canvas_width:
        x = canvas_width - player_coords[2]  # Prevent moving right off the canvas
    if player_coords[3] + y > canvas_height:
        y = canvas_height - player_coords[3]  # Prevent moving down off the canvas

    # Move the player
    canvas.move(player, x, y)
    root.after(20, move_player)  # Call move_player every 20 ms for smooth movement

# Key press event handler
def on_key_press(event):
    if event.keysym in move_directions:
        move_directions[event.keysym] = True

# Key release event handler
def on_key_release(event):
    if event.keysym in move_directions:
        move_directions[event.keysym] = False

# Bind key events
root.bind('<KeyPress>', on_key_press)
root.bind('<KeyRelease>', on_key_release)

# Start the movement loop
move_player()

# Run the main loop
root.mainloop()
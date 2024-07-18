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

# Movement functions
def move_Player(event):
    x, y = 0, 0
    if event.keysym == 'w':
        y = -10
    elif event.keysym == 's':
        y = 10
    elif event.keysym == 'a':
        x = -10
    elif event.keysym == 'd':
        x = 10
    canvas.move(player, x, y)

# Bind WASD keys to the movement functions
root.bind('<w>', move_Player)
root.bind('<s>', move_Player)
root.bind('<a>', move_Player)
root.bind('<d>', move_Player)

# Run the main loop
root.mainloop()

import tkinter as tk
from player import Player

# Create the main window
root = tk.Tk()
root.title("Python-Game")

# Set up the canvas
canvas_width = 400
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Create a Player instance
player_size = 30
player_x = canvas_width // 2
player_y = canvas_height // 2
player = Player(canvas, player_x, player_y, player_size)

# Bind key events to the Player instance methods
root.bind('<KeyPress>', player.on_key_press)
root.bind('<KeyRelease>', player.on_key_release)
canvas.bind('<Motion>', player.on_mouse_motion)

# Start the movement loop
player.move()

# Run the main loop
root.mainloop()
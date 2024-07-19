import tkinter as tk
import math
import random
from player import Player

class StarField:
    def __init__(self, canvas, width, height, num_stars=100):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.num_stars = num_stars
        self.stars = []
        self.create_stars()
        self.move_stars()

    def create_stars(self):
        """Create a set of stars at random positions."""
        for _ in range(self.num_stars):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 3)  # Small size for stars
            star = self.canvas.create_oval(x, y, x + size, y + size, fill='white', outline='white')
            self.stars.append((star, x, y))

    def move_stars(self):
        """Move stars to simulate a scrolling effect."""
        for star, x, y in self.stars:
            new_x = (x - 2) % self.width  # Move stars to the left and wrap around
            self.canvas.coords(star, new_x, y, new_x + 3, y + 3)  # Adjust size here if needed
        self.canvas.after(30, self.move_stars)  # Update stars every 30 ms

# Create the main window
root = tk.Tk()
root.title("Python-Game")

# Set up the canvas
canvas_width = 800
canvas_height = 800
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Create the star field background
star_field = StarField(canvas, canvas_width, canvas_height)

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
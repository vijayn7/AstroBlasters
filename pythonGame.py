import tkinter as tk

class Player:
    def __init__(self, canvas, x, y, size, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.move_directions = {'w': False, 's': False, 'a': False, 'd': False}
        # Create player rectangle
        self.player = canvas.create_rectangle(
            x - size // 2, 
            y - size // 2, 
            x + size // 2, 
            y + size // 2, 
            fill=color
        )
        self.isMoving = False

    def getPlayerCoords(self):
        return self.canvas.coords(self.player)

    def is_moving(self):
        """Return True if the player is currently moving, otherwise False."""
        return any(self.move_directions.values())

    def move(self):
        x_Velocity, y_Velocity = 0, 0
        if self.move_directions['w']:
            y_Velocity = -5
        if self.move_directions['s']:
            y_Velocity = 5
        if self.move_directions['a']:
            x_Velocity = -5
        if self.move_directions['d']:
            x_Velocity = 5

        # Get the current position of the player
        player_coords = self.getPlayerCoords()

        # Check for canvas boundaries
        if player_coords[0] + x_Velocity < 0:
            x_Velocity = -player_coords[0]  # Prevent moving left off the canvas
        if player_coords[1] + y_Velocity < 0:
            y_Velocity = -player_coords[1]  # Prevent moving up off the canvas
        if player_coords[2] + x_Velocity > self.canvas.winfo_width():
            x_Velocity = self.canvas.winfo_width() - player_coords[2]  # Prevent moving right off the canvas
        if player_coords[3] + y_Velocity > self.canvas.winfo_height():
            y_Velocity = self.canvas.winfo_height() - player_coords[3]  # Prevent moving down off the canvas

        # Move the player
        if (self.isMoving):
            self.canvas.Momove(self.player, x_Velocity, y_Velocity)
        
        # Update isMoving based on current movement directions
        self.isMoving = self.is_moving()
        
        self.canvas.after(20, self.move)  # Call move every 20 ms for smooth movement

    def on_key_press(self, event):
        if event.keysym in self.move_directions:
            self.move_directions[event.keysym] = True
            self.isMoving = self.is_moving()

    def on_key_release(self, event):
        if event.keysym in self.move_directions:
            self.move_directions[event.keysym] = False
            self.isMoving = self.is_moving()

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
player = Player(canvas, player_x, player_y, player_size, "blue")

# Bind key events to the Player instance methods
root.bind('<KeyPress>', player.on_key_press)
root.bind('<KeyRelease>', player.on_key_release)

# Start the movement loop
player.move()

# Run the main loop
root.mainloop()

import tkinter as tk
import math

class Player:
    def __init__(self, canvas, x, y, size, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.angle = 0  # Angle in degrees to represent direction
        self.move_directions = {'w': False, 's': False, 'a': False, 'd': False}
        # Create player triangle
        self.player = self.create_triangle(x, y, size, color)
        self.isMoving = False
        self.canvas.update()  # Ensure the canvas is updated to get correct dimensions

    def create_triangle(self, x, y, size, color):
        """Create a triangle representing the player at the given position."""
        angle_rad = math.radians(self.angle)
        # Calculate triangle points based on angle and size
        point1 = (x + size * math.cos(angle_rad), y + size * math.sin(angle_rad))
        point2 = (x + size * math.cos(angle_rad + 2.5 * math.pi / 3), y + size * math.sin(angle_rad + 2.5 * math.pi / 3))
        point3 = (x + size * math.cos(angle_rad - 2.5 * math.pi / 3), y + size * math.sin(angle_rad - 2.5 * math.pi / 3))
        return self.canvas.create_polygon(point1, point2, point3, fill=color)

    def getPlayerCoords(self):
        return self.canvas.coords(self.player)

    def is_moving(self):
        """Return True if the player is currently moving, otherwise False."""
        return any(self.move_directions.values())

    def update_angle(self, mouse_x, mouse_y):
        """Update the angle based on the mouse position."""
        # Calculate angle in radians and convert to degrees
        self.angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))
        self.redraw()

    def redraw(self):
        """Redraw the player triangle based on the current angle."""
        self.canvas.delete(self.player)
        self.player = self.create_triangle(self.x, self.y, self.size, self.color)

    def move(self):
        x_velocity, y_velocity = 0, 0
        if self.move_directions['w']:
            y_velocity = -5
        if self.move_directions['s']:
            y_velocity = 5
        if self.move_directions['a']:
            x_velocity = -5
        if self.move_directions['d']:
            x_velocity = 5

        # Move the player
        self.x += x_velocity
        self.y += y_velocity

        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Debugging output
        # print(f"Player position before boundary check: ({self.x}, {self.y})")
        # print(f"Canvas size: {canvas_width}x{canvas_height}")

        # Check for canvas boundaries
        if self.x - self.size // 2 < 0:
            self.x = self.size // 2
        if self.y - self.size // 2 < 0:
            self.y = self.size // 2
        if self.x + self.size // 2 > canvas_width:
            self.x = canvas_width - self.size // 2
        if self.y + self.size // 2 > canvas_height:
            self.y = canvas_height - self.size // 2

        # Debugging output
        # print(f"Player position after boundary check: ({self.x}, {self.y})")

        # Redraw the player at the new position
        self.redraw()

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

    def on_mouse_motion(self, event):
        """Update player direction based on mouse position."""
        self.update_angle(event.x, event.y)

# Main script to create window and run the game
def main():
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
    canvas.bind('<Motion>', player.on_mouse_motion)

    # Start the movement loop
    player.move()

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()

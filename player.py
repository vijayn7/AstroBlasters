import tkinter as tk
import math

class Player:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.angle = 0  # Angle in degrees to represent direction
        self.move_directions = {'w': False, 's': False, 'a': False, 'd': False}
        self.mouse_x = x  # Initialize mouse_x to player's start position
        self.mouse_y = y  # Initialize mouse_y to player's start position
        # Create player triangle
        self.player = self.create_triangle(x, y, size)
        self.isMoving = False
        self.canvas.update()  # Ensure the canvas is updated to get correct dimensions

    def create_triangle(self, x, y, size):
        """Create a polygon object to represent the player."""
        angle_rad = math.radians(self.angle)
        # Calculate triangle points based on angle and size
        point1 = (x + size * math.cos(angle_rad), y + size * math.sin(angle_rad))
        point2 = (x + size * math.cos(angle_rad + 2 * math.pi / 3), y + size * math.sin(angle_rad + 2 * math.pi / 3))
        point3 = (x + size * math.cos(angle_rad - 2 * math.pi / 3), y + size * math.sin(angle_rad - 2 * math.pi / 3))

        # Create a multicolored triangle by drawing each side separately
        return [
            self.canvas.create_line(point1, point2, fill='red', width=2),
            self.canvas.create_line(point2, point3, fill='green', width=2),
            self.canvas.create_line(point3, point1, fill='blue', width=2)
        ]

    def getPlayerCoords(self):
        return self.canvas.coords(self.player[0])

    def is_moving(self):
        """Return True if the player is currently moving, otherwise False."""
        return any(self.move_directions.values())

    def update_angle(self):
        """Update the angle based on the mouse position."""
        # Calculate angle in radians and convert to degrees
        self.angle = math.degrees(math.atan2(self.mouse_y - self.y, self.mouse_x - self.x))
        self.redraw()

    def redraw(self):
        """Redraw the player triangle based on the current angle."""
        for line in self.player:
            self.canvas.delete(line)  # Remove the existing lines

        angle_rad = math.radians(self.angle)
        # Calculate triangle points based on angle and size
        point1 = (self.x + self.size * math.cos(angle_rad), self.y + self.size * math.sin(angle_rad))
        point2 = (self.x + self.size * math.cos(angle_rad + 2 * math.pi / 3), self.y + self.size * math.sin(angle_rad + 2 * math.pi / 3))
        point3 = (self.x + self.size * math.cos(angle_rad - 2 * math.pi / 3), self.y + self.size * math.sin(angle_rad - 2 * math.pi / 3))
        
        # Create new lines for the multicolored triangle
        self.player = [
            self.canvas.create_line(point1, point2, fill='red', width=2),
            self.canvas.create_line(point2, point3, fill='green', width=2),
            self.canvas.create_line(point3, point1, fill='blue', width=2)
        ]

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

        # Check for canvas boundaries
        if self.x - self.size < 0:
            self.x = self.size
        if self.y - self.size < 0:
            self.y = self.size
        if self.x + self.size > canvas_width:
            self.x = canvas_width - self.size
        if self.y + self.size > canvas_height:
            self.y = canvas_height - self.size

        # Update the angle based on the current mouse position
        self.update_angle()

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
        """Update mouse position for direction calculation."""
        self.mouse_x = event.x
        self.mouse_y = event.y
import tkinter as tk
import math

class Laser:
    def __init__(self, canvas, x, y, angle):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.size = 10  # Size of the laser
        self.speed = 10  # Speed of the laser
        self.laser = self.create_laser()

    def create_laser(self):
        """Create a laser line at the given position and angle."""
        angle_rad = math.radians(self.angle)
        x_end = self.x + self.size * math.cos(angle_rad)
        y_end = self.y + self.size * math.sin(angle_rad)
        return self.canvas.create_line(self.x, self.y, x_end, y_end, fill="yellow", width=2)

    def move(self):
        """Move the laser and bounce off walls."""
        angle_rad = math.radians(self.angle)
        x_velocity = self.speed * math.cos(angle_rad)
        y_velocity = self.speed * math.sin(angle_rad)

        self.x += x_velocity
        self.y += y_velocity

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Check for wall collisions and bounce
        if self.x <= 0 or self.x >= canvas_width:
            self.angle = 180 - self.angle
        if self.y <= 0 or self.y >= canvas_height:
            self.angle = -self.angle

        self.canvas.coords(self.laser, self.x, self.y, self.x + x_velocity, self.y + y_velocity)

        # Remove the laser if it goes out of bounds
        if (self.x < 0 or self.x > canvas_width or
            self.y < 0 or self.y > canvas_height):
            self.canvas.delete(self.laser)
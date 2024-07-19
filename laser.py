import tkinter as tk
import math

class Laser:
    def __init__(self, canvas, x, y, angle):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.size = 30  # Size of the laser
        self.speed = 10  # Speed of the laser
        self.bounces = 3  # Maximum number of bounces
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

        bounced = False

        if self.x <= 0:
            self.x = 0
            self.angle = 180 - self.angle
            bounced = True
        if self.x >= canvas_width:
            self.x = canvas_width
            self.angle = 180 - self.angle
            bounced = True
        if self.y <= 0:
            self.y = 0
            self.angle = -self.angle
            bounced = True
        if self.y >= canvas_height:
            self.y = canvas_height
            self.angle = -self.angle
            bounced = True

        if bounced:
            self.bounces -= 1
            if self.bounces <= 0:
                self.canvas.delete(self.laser)
                return

        # Update the laser line
        angle_rad = math.radians(self.angle)
        x_end = self.x + self.size * math.cos(angle_rad)
        y_end = self.y + self.size * math.sin(angle_rad)
        self.canvas.coords(self.laser, self.x, self.y, x_end, y_end)

        # Continue moving the laser
        self.canvas.after(20, self.move)
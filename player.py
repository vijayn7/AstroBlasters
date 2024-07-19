import tkinter as tk
import math
from laser import Laser
import time  # For cooldown timer

class Player:
    def __init__(self, canvas, x, y, size, mode):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.angle = 0
        self.move_directions = {'w': False, 's': False, 'a': False, 'd': False}
        self.mouse_x = x
        self.mouse_y = y
        self.lasers = []
        self.mode = mode  # Store the game mode

        # Cooldown attributes
        self.last_shot_time = 0
        self.cooldown_period = 1  # Cooldown period in seconds
        self.cooldown_bar_width = 80  # Reduced width
        self.cooldown_bar_height = 8   # Reduced height

        # Create player triangle
        self.player = self.create_triangle(x, y, size)

        # Draw cooldown bar background and active portion
        self.cooldown_bar_bg = self.canvas.create_rectangle(
            self.x - self.cooldown_bar_width // 2,
            self.y + self.size + 20,
            self.x + self.cooldown_bar_width // 2,
            self.y + self.size + 20 + self.cooldown_bar_height,
            fill="gray", outline="gray"
        )
        self.cooldown_bar_fg = self.canvas.create_rectangle(
            self.x - self.cooldown_bar_width // 2,
            self.y + self.size + 20,
            self.x - self.cooldown_bar_width // 2,
            self.y + self.size + 20 + self.cooldown_bar_height,
            fill="green", outline="green"
        )
        self.update_cooldown_bar()

        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.on_mouse_click)

    def create_triangle(self, x, y, size):
        angle_rad = math.radians(self.angle)
        point1 = (x + size * math.cos(angle_rad), y + size * math.sin(angle_rad))
        point2 = (x + size * math.cos(angle_rad + 2 * math.pi / 3), y + size * math.sin(angle_rad + 2 * math.pi / 3))
        point3 = (x + size * math.cos(angle_rad - 2 * math.pi / 3), y + size * math.sin(angle_rad - 2 * math.pi / 3))

        return [
            self.canvas.create_line(point1, point2, fill='red', width=2),
            self.canvas.create_line(point2, point3, fill='green', width=2),
            self.canvas.create_line(point3, point1, fill='blue', width=2)
        ]

    def update_cooldown_bar(self):
        """Update the cooldown bar to show the remaining cooldown time."""
        elapsed_time = time.time() - self.last_shot_time
        fill_width = min(elapsed_time, self.cooldown_period) * self.cooldown_bar_width / self.cooldown_period
        self.canvas.coords(self.cooldown_bar_fg,
            self.x - self.cooldown_bar_width // 2,
            self.y + self.size + 20,
            self.x - self.cooldown_bar_width // 2 + fill_width,
            self.y + self.size + 20 + self.cooldown_bar_height
        )
        if elapsed_time < self.cooldown_period:
            self.canvas.after(50, self.update_cooldown_bar)  # Update every 50 ms

    def shoot_laser(self):
        """Shoot a laser if cooldown period has passed."""
        current_time = time.time()
        if current_time - self.last_shot_time >= self.cooldown_period:
            self.lasers.append(Laser(self.canvas, self.x, self.y, self.angle, self.mode))
            self.last_shot_time = current_time
            self.update_cooldown_bar()  # Update cooldown bar after shooting

    def on_key_press(self, event):
        if event.keysym in self.move_directions:
            self.move_directions[event.keysym] = True
            self.isMoving = self.is_moving()
    
    def on_key_release(self, event):
        if event.keysym in self.move_directions:
            self.move_directions[event.keysym] = False
            self.isMoving = self.is_moving()
    
    def on_mouse_motion(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def on_mouse_click(self, event):
        self.shoot_laser()

    def is_moving(self):
        return any(self.move_directions.values())

    def update_angle(self):
        self.angle = math.degrees(math.atan2(self.mouse_y - self.y, self.mouse_x - self.x))
        self.redraw()

    def redraw(self):
        for line in self.player:
            self.canvas.delete(line)
        angle_rad = math.radians(self.angle)
        point1 = (self.x + self.size * math.cos(angle_rad), self.y + self.size * math.sin(angle_rad))
        point2 = (self.x + self.size * math.cos(angle_rad + 2 * math.pi / 3), self.y + self.size * math.sin(angle_rad + 2 * math.pi / 3))
        point3 = (self.x + self.size * math.cos(angle_rad - 2 * math.pi / 3), self.y + self.size * math.sin(angle_rad - 2 * math.pi / 3))
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

        self.x += x_velocity
        self.y += y_velocity

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if self.x - self.size < 0:
            self.x = self.size
        if self.y - self.size < 0:
            self.y = self.size
        if self.x + self.size > canvas_width:
            self.x = canvas_width - self.size
        if self.y + self.size > canvas_height:
            self.y = canvas_height - self.size

        self.update_angle()
        self.isMoving = self.is_moving()

        for laser in self.lasers:
            laser.move()

        self.lasers = [laser for laser in self.lasers if self.canvas.coords(laser.laser)]
        self.canvas.after(20, self.move)

import math
import random

class Enemy:
    def __init__(self, canvas, x, y, player_x, player_y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.player_x = player_x
        self.player_y = player_y
        self.speed = 2  # Default speed, can be overridden by subclasses
        self.shape = None  # To be defined by subclasses
        self.shape_type = None  # To be defined by subclasses
        self.movement_type = "straight"  # Default movement type
        self.create_shape()

    def create_shape(self):
        """Create the enemy's shape. To be implemented by subclasses."""
        pass

    def move(self):
        """Move the enemy according to its movement type and log its position."""
        if self.movement_type == "straight":
            angle_rad = math.atan2(self.player_y - self.y, self.player_x - self.x)
            self.x += self.speed * math.cos(angle_rad)
            self.y += self.speed * math.sin(angle_rad)
        elif self.movement_type == "zigzag":
            # Example of zigzag movement
            angle_rad = math.atan2(self.player_y - self.y, self.player_x - self.x)
            zigzag_angle = angle_rad + (0.2 * math.sin(random.uniform(0, 2 * math.pi)))
            self.x += self.speed * math.cos(zigzag_angle)
            self.y += self.speed * math.sin(zigzag_angle)
        elif self.movement_type == "circular":
            # Move in a circular path around the player
            angle_to_player = math.atan2(self.player_y - self.y, self.player_x - self.x)
            radius = 100  # Fixed radius for circular movement
            angle_rad = math.atan2(self.y - self.player_y, self.x - self.player_x) + self.speed / radius
            self.x = self.player_x + radius * math.cos(angle_rad)
            self.y = self.player_y + radius * math.sin(angle_rad)

        # Log the enemy's position for debugging
        print(f"Enemy {self.__class__.__name__} - Position: ({self.x:.2f}, {self.y:.2f})")

        if self.shape:
            # Update coordinates based on shape type
            if self.shape_type == "oval":
                self.canvas.coords(self.shape, self.x - 10, self.y - 10, self.x + 10, self.y + 10)
            elif self.shape_type == "rectangle":
                self.canvas.coords(self.shape, self.x - 15, self.y - 15, self.x + 15, self.y + 15)
            elif self.shape_type == "polygon":
                self.canvas.coords(self.shape, self.x - 10, self.y - 10, self.x + 10, self.y - 10, self.x, self.y + 10)
    
    def is_out_of_bounds(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        return not (0 <= self.x <= canvas_width and 0 <= self.y <= canvas_height)

class BasicDrone(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.movement_type = "straight"  # Example movement type

    def create_shape(self):
        self.shape_type = "oval"
        self.shape = self.canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="blue")

class FastScout(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 4  # Faster speed
        self.movement_type = "zigzag"

    def create_shape(self):
        self.shape_type = "oval"
        self.shape = self.canvas.create_oval(self.x - 8, self.y - 8, self.x + 8, self.y + 8, fill="green")

class ArmoredTank(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 1  # Slower speed
        self.movement_type = "straight"

    def create_shape(self):
        self.shape_type = "rectangle"
        self.shape = self.canvas.create_rectangle(self.x - 15, self.y - 15, self.x + 15, self.y + 15, fill="red")

class CamouflagedStealth(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.movement_type = "zigzag"

    def create_shape(self):
        self.shape_type = "oval"
        self.shape = self.canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="gray")

class SuicideBomber(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 2
        self.movement_type = "straight"

    def create_shape(self):
        self.shape_type = "polygon"
        self.shape = self.canvas.create_polygon(self.x - 10, self.y - 10, self.x + 10, self.y - 10, self.x, self.y + 10, fill="purple")

class FighterJet(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 3
        self.movement_type = "zigzag"

    def create_shape(self):
        self.shape_type = "polygon"
        self.shape = self.canvas.create_polygon(self.x - 10, self.y - 10, self.x + 10, self.y, self.x - 10, self.y + 10, fill="white")

    def move(self):
        # Example of zigzag movement
        angle_rad = math.atan2(self.player_y - self.y, self.player_x - self.x)
        zigzag_angle = angle_rad + (0.3 * math.sin(self.x / 50))  # Adjust for more/less zigzag
        self.x += self.speed * math.cos(zigzag_angle)
        self.y += self.speed * math.sin(zigzag_angle)

        # Update the enemy's position on the canvas
        self.canvas.coords(self.shape, self.x - 10, self.y - 10, self.x + 10, self.y, self.x - 10, self.y + 10)

class EliteGuardian(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 2
        self.movement_type = "zigzag"

    def create_shape(self):
        self.shape_type = "rectangle"
        self.shape = self.canvas.create_rectangle(self.x - 12, self.y - 12, self.x + 12, self.y + 12, fill="gold")

    def move(self):
        # Example of zigzag movement
        angle_rad = math.atan2(self.player_y - self.y, self.player_x - self.x)
        zigzag_angle = angle_rad + (0.3 * math.sin(self.x / 50))  # Adjust for more/less zigzag
        self.x += self.speed * math.cos(zigzag_angle)
        self.y += self.speed * math.sin(zigzag_angle)

        # Update the enemy's position on the canvas
        self.canvas.coords(self.shape, self.x - 12, self.y - 12, self.x + 12, self.y + 12)

class SwarmDrone(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 2
        self.movement_type = "zigzag"

    def create_shape(self):
        self.shape_type = "oval"
        self.shape = self.canvas.create_oval(self.x - 6, self.y - 6, self.x + 6, self.y + 6, fill="cyan")
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
        self.health = 100  # Default health, can be overridden by subclasses
        self.max_health = self.health
        self.create_shape()
        self.health_bar = self.create_health_bar()

    def create_shape(self):
        """Create the enemy's shape. To be implemented by subclasses."""
        pass

    def create_health_bar(self):
        """Create the health bar above the enemy."""
        if not self.shape:
            return None  # Return None if the shape has not been created

        coords = self.canvas.coords(self.shape)
        if len(coords) != 4:
            return None  # Return None if coordinates are not valid

        x0, y0, x1, y1 = coords
        health_bar_y = y0 - 10  # Position the health bar above the enemy
        return self.canvas.create_rectangle(x0, health_bar_y, x1, health_bar_y + 5, fill="green", outline="")

    def update_health_bar(self):
        """Update the health bar to reflect current health."""
        if not self.health_bar:
            return  # If health bar was not created, do nothing

        coords = self.canvas.coords(self.shape)
        if len(coords) != 4:
            return  # If coordinates are not valid, do nothing

        x0, y0, x1, y1 = coords
        health_ratio = self.health / self.max_health
        # Calculate the new end position of the health bar
        new_width = (x1 - x0) * health_ratio
        # Update the health bar position
        self.canvas.coords(self.health_bar, x0, y0 - 10, x0 + new_width, y0 - 5)

        # Change color from green to red as health decreases
        red = int(255 * (1 - health_ratio))
        green = int(255 * health_ratio)
        self.canvas.itemconfig(self.health_bar, fill=f'#{red:02x}{green:02x}00')

    def move(self):
        """Move the enemy according to its movement type."""
        if self.movement_type == "straight":
            angle_rad = math.atan2(self.player_y - self.y, self.player_x - self.x)
            self.x += self.speed * math.cos(angle_rad)
            self.y += self.speed * math.sin(angle_rad)
        elif self.movement_type == "zigzag":
            angle_rad = math.atan2(self.player_y - self.y, self.player_x - self.x)
            zigzag_angle = angle_rad + (0.2 * math.sin(random.uniform(0, 2 * math.pi)))
            self.x += self.speed * math.cos(zigzag_angle)
            self.y += self.speed * math.sin(zigzag_angle)

        if self.shape:
            if self.shape_type == "oval":
                self.canvas.coords(self.shape, self.x - 10, self.y - 10, self.x + 10, self.y + 10)
            elif self.shape_type == "rectangle":
                self.canvas.coords(self.shape, self.x - 15, self.y - 15, self.x + 15, self.y + 15)
            elif self.shape_type == "polygon":
                self.canvas.coords(self.shape, self.x - 10, self.y - 10, self.x + 10, self.y, self.x - 10, self.y + 10)
            
            # Update the health bar position and appearance
            self.update_health_bar()
    
    def take_damage(self, damage):
        """Reduce enemy health and update the health bar."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.destroy()
        else:
            self.update_health_bar()

    def destroy(self):
        """Destroy the enemy and remove from canvas."""
        self.canvas.delete(self.shape)
        self.canvas.delete(self.health_bar)

    def is_out_of_bounds(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        return not (0 <= self.x <= canvas_width and 0 <= self.y <= canvas_height)


class BasicDrone(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.movement_type = "straight"
        self.health = 50  # Example health for BasicDrone
        self.max_health = self.health

    def create_shape(self):
        self.shape_type = "oval"
        self.shape = self.canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="blue")


class FastScout(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 4
        self.movement_type = "zigzag"
        self.health = 30  # Less health for faster enemy
        self.max_health = self.health

    def create_shape(self):
        self.shape_type = "oval"
        self.shape = self.canvas.create_oval(self.x - 8, self.y - 8, self.x + 8, self.y + 8, fill="green")


class ArmoredTank(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 1
        self.movement_type = "straight"
        self.health = 150  # More health for armored enemy
        self.max_health = self.health

    def create_shape(self):
        self.shape_type = "rectangle"
        self.shape = self.canvas.create_rectangle(self.x - 15, self.y - 15, self.x + 15, self.y + 15, fill="red")


class FighterJet(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 3
        self.movement_type = "zigzag"
        self.health = 80
        self.max_health = self.health

    def create_shape(self):
        self.shape_type = "polygon"
        self.shape = self.canvas.create_polygon(self.x - 10, self.y - 10, self.x + 10, self.y, self.x - 10, self.y + 10, fill="white")
        # Ensure the health bar is created after the shape
        self.health_bar = self.create_health_bar()

class CamouflagedStealth(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.movement_type = "zigzag"
        self.health = 60
        self.max_health = self.health

    def create_shape(self):
        self.shape_type = "oval"
        self.shape = self.canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="gray")


class SuicideBomber(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 2
        self.movement_type = "straight"
        self.health = 40
        self.max_health = self.health

    def create_shape(self):
        self.shape_type = "polygon"
        self.shape = self.canvas.create_polygon(self.x - 10, self.y - 10, self.x + 10, self.y - 10, self.x, self.y + 10, fill="purple")
        # Ensure the health bar is created after the shape
        self.health_bar = self.create_health_bar()

class EliteGuardian(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 1
        self.movement_type = "zigzag"
        self.health = 120
        self.max_health = self.health

    def create_shape(self):
        self.shape_type = "rectangle"
        self.shape = self.canvas.create_rectangle(self.x - 12, self.y - 12, self.x + 12, self.y + 12, fill="gold")


class SwarmDrone(Enemy):
    def __init__(self, canvas, x, y, player_x, player_y):
        super().__init__(canvas, x, y, player_x, player_y)
        self.speed = 3
        self.movement_type = "zigzag"
        self.health = 20
        self.max_health = self.health

    def create_shape(self):
        self.shape_type = "oval"
        self.shape = self.canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill="pink")
import math

class Laser:
    def __init__(self, canvas, x, y, angle, mode):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.size = 30
        self.speed = 10
        self.bounces = 3  # Maximum number of bounces (not used in Orbital Defense)
        self.mode = mode
        self.laser = self.create_laser()
        self.exists = True  # Flag to check if the laser still exists
        self.damage = 50  # Damage value for testing purposes

    def create_laser(self):
        angle_rad = math.radians(self.angle)
        x_end = self.x + self.size * math.cos(angle_rad)
        y_end = self.y + self.size * math.sin(angle_rad)
        return self.canvas.create_line(self.x, self.y, x_end, y_end, fill="yellow", width=2)

    def move(self):
        angle_rad = math.radians(self.angle)
        x_velocity = self.speed * math.cos(angle_rad)
        y_velocity = self.speed * math.sin(angle_rad)

        self.x += x_velocity
        self.y += y_velocity

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if self.mode == "Orbital Defense":
            if self.x <= 0 or self.x >= canvas_width or self.y <= 0 or self.y >= canvas_height:
                self.canvas.delete(self.laser)
                self.exists = False
                return
        else:
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
                    self.exists = False
                    return

        angle_rad = math.radians(self.angle)
        x_end = self.x + self.size * math.cos(angle_rad)
        y_end = self.y + self.size * math.sin(angle_rad)
        self.canvas.coords(self.laser, self.x, self.y, x_end, y_end)

        self.check_collision()

        # Schedule the next move
        self.canvas.after(20, self.move)

    def check_collision(self):
        # Check collision with enemies
        for enemy_id in self.canvas.find_withtag("enemy"):
            enemy_coords = self.canvas.coords(enemy_id)
            if self.is_collision(enemy_coords):
                print(f"Collision detected with enemy ID: {enemy_id}")
                self.apply_damage(enemy_id)
                self.canvas.delete(self.laser)
                self.exists = False
                break

    def is_collision(self, enemy_coords):
        # Check if the laser intersects with a triangular enemy
        if len(enemy_coords) != 6:
            print(f"Invalid enemy coordinates for triangle: {enemy_coords}")
            return False

        x1, y1, x2, y2, x3, y3 = enemy_coords
        laser_coords = self.canvas.coords(self.laser)
        if len(laser_coords) != 4:
            print(f"Invalid laser coordinates: {laser_coords}")
            return False

        lx1, ly1, lx2, ly2 = laser_coords

        # Check if the laser intersects any of the triangle's sides
        def on_segment(px, py, qx, qy, rx, ry):
            """Check if point (rx, ry) lies on line segment (px, py) - (qx, qy)."""
            return (min(px, qx) <= rx <= max(px, qx)) and (min(py, qy) <= ry <= max(py, qy))

        def orientation(px, py, qx, qy, rx, ry):
            """Find the orientation of the ordered triplet (px, py), (qx, qy), (rx, ry)."""
            val = (qy - py) * (rx - qx) - (qx - px) * (ry - qy)
            if val == 0:
                return 0  # collinear
            return 1 if val > 0 else 2  # clockwise or counterclockwise

        def do_intersect(p1x, p1y, q1x, q1y, p2x, p2y, q2x, q2y):
            """Check if line segments (p1x, p1y) - (q1x, q1y) and (p2x, p2y) - (q2x, q2y) intersect."""
            o1 = orientation(p1x, p1y, q1x, q1y, p2x, p2y)
            o2 = orientation(p1x, p1y, q1x, q1y, q2x, q2y)
            o3 = orientation(p2x, p2y, q2x, q2y, p1x, p1y)
            o4 = orientation(p2x, p2y, q2x, q2y, q1x, q1y)

            if o1 != o2 and o3 != o4:
                return True

            if o1 == 0 and on_segment(p1x, p1y, q1x, q1y, p2x, p2y):
                return True
            if o2 == 0 and on_segment(p1x, p1y, q1x, q1y, q2x, q2y):
                return True
            if o3 == 0 and on_segment(p2x, p2y, q2x, q2y, p1x, p1y):
                return True
            if o4 == 0 and on_segment(p2x, p2y, q2x, q2y, q1x, q1y):
                return True

            return False

        collision = (
            do_intersect(lx1, ly1, lx2, ly2, x1, y1, x2, y2) or
            do_intersect(lx1, ly1, lx2, ly2, x2, y2, x3, y3) or
            do_intersect(lx1, ly1, lx2, ly2, x3, y3, x1, y1)
        )

        if collision:
            print(f"Laser intersects with triangular enemy: ({x1}, {y1}, {x2}, {y2}, {x3}, {y3})")
        
        return collision

    def apply_damage(self, enemy_id):
        # Find the enemy instance by ID and apply damage
        enemy_coords = self.canvas.coords(enemy_id)
        print(f"Attempting to apply damage to enemy ID: {enemy_id} with coordinates: {enemy_coords}")
        
        # Look for enemy with the given ID
        if enemy_id in self.canvas.find_withtag("enemy"):
            enemy_instance = self.canvas.find_withtag(enemy_id)[0]
            # Check if the enemy instance has 'take_damage' method
            if hasattr(enemy_instance, 'take_damage'):
                enemy_instance.take_damage(self.damage)
            else:
                print(f"Enemy with ID {enemy_id} does not have 'take_damage' method.")
        else:
            print(f"Enemy with ID {enemy_id} not found.")

    def delete(self):
        if self.exists:
            self.canvas.delete(self.laser)
            self.exists = False

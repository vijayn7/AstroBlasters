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
        for enemy in self.canvas.find_withtag("enemy"):
            if self.is_collision(enemy):
                self.apply_damage(enemy)
                self.canvas.delete(self.laser)
                self.exists = False
                break

    def is_collision(self, enemy):
        # Check if the laser intersects with the enemy
        enemy_coords = self.canvas.coords(enemy)
        if len(enemy_coords) < 4:
            print(f"Invalid enemy coordinates: {enemy_coords}")
            return False

        x0, y0, x1, y1 = enemy_coords

        laser_coords = self.canvas.coords(self.laser)
        if len(laser_coords) != 4:
            print(f"Invalid laser coordinates: {laser_coords}")
            return False

        lx0, ly0, lx1, ly1 = laser_coords

        # Check bounding box collision
        box_collision = not (lx1 < x0 or lx0 > x1 or ly1 < y0 or ly0 > y1)
        if not box_collision:
            return False

        # Check line intersection (if bounding box collision detected)
        def is_point_inside(px, py):
            return x0 <= px <= x1 and y0 <= py <= y1

        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        def lines_intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

        def line_box_intersect(lx0, ly0, lx1, ly1, x0, y0, x1, y1):
            box_corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            for i in range(4):
                next_i = (i + 1) % 4
                if lines_intersect((lx0, ly0), (lx1, ly1), box_corners[i], box_corners[next_i]):
                    return True
            return is_point_inside(lx0, ly0) or is_point_inside(lx1, ly1)

        collision = line_box_intersect(lx0, ly0, lx1, ly1, x0, y0, x1, y1)

        if collision:
            print(f"Laser intersects with enemy: ({x0}, {y0}, {x1}, {y1})")

        return collision

    def apply_damage(self, enemy):
        # Find the enemy instance and apply damage
        for item in self.canvas.find_withtag("enemy"):
            if item == enemy:
                enemy_instance = self.canvas.find_withtag(item)[0]
                enemy_instance.apply_damage(self.damage)

    def delete(self):
        if self.exists:
            self.canvas.delete(self.laser)
            self.exists = False

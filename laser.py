# laser.py

import math
from enemy import Enemy

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
        self.enemy_map = Enemy.get_enemy_map()  # Retrieve enemy_map from Enemy class

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
                self.delete()
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
                    self.delete()
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
            enemy = self.enemy_map.get(enemy_id)
            if enemy:
                enemy_coords = self.canvas.coords(enemy_id)
                if self.is_collision(enemy_coords):
                    print(f"Collision detected with enemy ID: {enemy_id}")
                    self.apply_damage(enemy_id)
                    self.delete()
                    self.exists = False
                    break

    def is_collision(self, enemy_coords):
        # Determine the type of enemy by checking the number of coordinates
        if len(enemy_coords) == 6:  # Triangle
            return self.check_triangle_collision(enemy_coords)
        elif len(enemy_coords) == 4:  # Rectangle
            return self.check_rectangle_collision(enemy_coords)
        elif len(enemy_coords) == 5:  # Oval
            return self.check_oval_collision(enemy_coords)
        else:
            return False

    def check_triangle_collision(self, coords):
        x1, y1, x2, y2, x3, y3 = coords
        laser_coords = self.canvas.coords(self.laser)
        lx1, ly1, lx2, ly2 = 0, 0, 0, 0
        try:
            lx1, ly1, lx2, ly2 = laser_coords
        except:
            return False

        # Check if the laser intersects any of the triangle's sides
        def on_segment(px, py, qx, qy, rx, ry):
            return (min(px, qx) <= rx <= max(px, qx)) and (min(py, qy) <= ry <= max(py, qy))

        def orientation(px, py, qx, qy, rx, ry):
            val = (qy - py) * (rx - qx) - (qx - px) * (ry - qy)
            if val == 0:
                return 0  # collinear
            return 1 if val > 0 else 2  # clockwise or counterclockwise

        def do_intersect(p1x, p1y, q1x, q1y, p2x, p2y, q2x, q2y):
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

        return (
            do_intersect(lx1, ly1, lx2, ly2, x1, y1, x2, y2) or
            do_intersect(lx1, ly1, lx2, ly2, x2, y2, x3, y3) or
            do_intersect(lx1, ly1, lx2, ly2, x3, y3, x1, y1)
        )

    def check_rectangle_collision(self, rect_coords):
        if len(rect_coords) != 4:
            print(f"Error: Invalid rectangle coordinates: {rect_coords}")
            return False

        x1, y1, x2, y2 = rect_coords
        laser_coords = self.canvas.coords(self.laser)
        if len(laser_coords) != 4:
            # print(f"Error: Invalid laser coordinates: {laser_coords}")
            return False

        lx1, ly1, lx2, ly2 = laser_coords

        def line_intersect(x1, y1, x2, y2, lx1, ly1, lx2, ly2):
            def ccw(A, B, C):
                return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

            def intersect(A, B, C, D):
                return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

            A = (x1, y1)
            B = (x2, y2)
            C = (lx1, ly1)
            D = (lx2, ly2)
            return intersect(A, B, C, D) or intersect(C, D, A, B)

        # Check if laser intersects with any of the rectangle's edges
        return (
            line_intersect(x1, y1, x2, y1, lx1, ly1, lx2, ly2) or
            line_intersect(x2, y1, x2, y2, lx1, ly1, lx2, ly2) or
            line_intersect(x2, y2, x1, y2, lx1, ly1, lx2, ly2) or
            line_intersect(x1, y2, x1, y1, lx1, ly1, lx2, ly2)
        )

    def check_oval_collision(self, oval_coords):
        if len(oval_coords) != 4:
            print(f"Error: Invalid oval coordinates: {oval_coords}")
            return False

        x1, y1, x2, y2 = oval_coords
        laser_coords = self.canvas.coords(self.laser)
        if len(laser_coords) != 4:
            print(f"Error: Invalid laser coordinates: {laser_coords}")
            return False

        lx1, ly1, lx2, ly2 = laser_coords

        def point_inside_oval(px, py, cx1, cy1, cx2, cy2):
            center_x = (cx1 + cx2) / 2
            center_y = (cy1 + cy2) / 2
            a = (cx2 - cx1) / 2
            b = (cy2 - cy1) / 2
            return ((px - center_x) ** 2 / a ** 2) + ((py - center_y) ** 2 / b ** 2) <= 1

        def oval_intersect(lx1, ly1, lx2, ly2, cx1, cy1, cx2, cy2):
            return (point_inside_oval(lx1, ly1, cx1, cy1, cx2, cy2) or
                    point_inside_oval(lx2, ly2, cx1, cy1, cx2, cy2))

        return oval_intersect(lx1, ly1, lx2, ly2, x1, y1, x2, y2)

    def apply_damage(self, enemy_id):
        # Find the enemy instance by ID and apply damage
        enemy = self.enemy_map.get(enemy_id)
        if enemy:
            enemy.take_damage(self.damage)
            print(f"Applied {self.damage} damage to enemy ID: {enemy_id}")
        else:
            print(f"No enemy found for ID {enemy_id}")

    def delete(self):
        if self.exists:
            self.canvas.delete(self.laser)
            del self
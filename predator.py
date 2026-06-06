import math
from pyglet import shapes
from constants import (
    MOUSE_PREDATOR,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PREDATOR_RANGE,
    PREDATOR_SIZE,
    PREDATOR_SPEED,
    PREDATOR_PULL,
)

shapes.Triangle._anchor_y = -PREDATOR_SIZE

class Predator:
    def __init__(self, x, y, i, batch):
        self.shape = shapes.Triangle(
            x, y + PREDATOR_SIZE,
            x - PREDATOR_SIZE, y - PREDATOR_SIZE,
            x + PREDATOR_SIZE, y - PREDATOR_SIZE,
            color=(255, 230, 225),
            batch=batch
        )
        self.vx = PREDATOR_SPEED
        self.vy = PREDATOR_SPEED
        self.id = i

    def wrap_around(self, gap):
        if self.shape.x > WINDOW_WIDTH + gap:
            self.shape.x = 0 - gap
        elif self.shape.x < 0 - gap:
            self.shape.x = WINDOW_WIDTH + gap

        if self.shape.y > WINDOW_HEIGHT + gap:
            self.shape.y = 0 - gap
        elif self.shape.y < 0 - gap:
            self.shape.y = WINDOW_HEIGHT + gap

    def steer(self, target_vx, target_vy, factor):
        self.vx += factor * (target_vx)
        self.vy += factor * (target_vy)

    def stabalize_vel(self):
        velocity = math.sqrt(self.vx**2 + self.vy**2)
        if velocity == 0:
            target_vx = PREDATOR_SPEED
            target_vy = PREDATOR_SPEED
        else:
            target_vx = (self.vx / velocity) * PREDATOR_SPEED
            target_vy = (self.vy / velocity) * PREDATOR_SPEED

        self.steer(target_vx - self.vx, target_vy - self.vy, 0.2)

    def calculate_vel(self, boids):
        nearest_dst = PREDATOR_RANGE
        nearest_x = None
        nearest_y = None
        for boid in boids:
            dst_x = boid.shape.x - self.shape.x
            dst_y = boid.shape.y - self.shape.y
            dst = math.sqrt((dst_x)**2 + (dst_y)**2)
            if 0 < dst < PREDATOR_RANGE:
                if nearest_dst > dst:
                    nearest_x = dst_x
                    nearest_y = dst_y
                    nearest_dst = dst
        if nearest_dst < PREDATOR_RANGE:
            pull_x = nearest_x
            pull_y = nearest_y
            self.steer(pull_x, pull_y, PREDATOR_PULL)

    def update(self, dt, boids, mouse_x, mouse_y):
        self.stabalize_vel()
        if self.id == 0 and MOUSE_PREDATOR == True:
            self.steer(mouse_x - self.shape.x, mouse_y - self.shape.y, 0.05)
        else:
            self.calculate_vel(boids)
 
        self.shape.x += self.vx * dt
        self.shape.y += self.vy * dt
        self.wrap_around(PREDATOR_SIZE)
        self.shape.rotation = -math.degrees(math.atan2(self.vy, self.vx)) + 90


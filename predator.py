import math
from pyglet import shapes
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PREDATOR_RANGE,
    PREDATOR_SIZE,
    PREDATOR_SPEED,
    PREDATOR_PULL,
)

shapes.Triangle._anchor_y = -PREDATOR_SIZE

class Predator:
    def __init__(self, x, y, batch):
        self.shape = shapes.Triangle(
            x, y + PREDATOR_SIZE,
            x - PREDATOR_SIZE, y - PREDATOR_SIZE,
            x + PREDATOR_SIZE, y - PREDATOR_SIZE,
            color=(255, 255, 255),
            batch=batch
        )
        self.vx = PREDATOR_SPEED
        self.vy = PREDATOR_SPEED

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

        self.vx += 0.2 * (target_vx - self.vx)
        self.vy += 0.2 * (target_vy - self.vy)


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
            pull_vx = nearest_x
            pull_vy = nearest_y
            self.steer(pull_vx, pull_vy, PREDATOR_PULL)

    def update(self, dt, boids):
        self.stabalize_vel()
        self.calculate_vel(boids)
 
        self.shape.x += self.vx * dt
        self.shape.y += self.vy * dt
        self.wrap_around(PREDATOR_SIZE)
        self.shape.rotation = -math.degrees(math.atan2(self.vy, self.vx)) + 90


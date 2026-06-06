import math
import random
from pyglet import shapes
from constants import (
    ALIGNMENT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BOID_SPEED,
    BOID_SIZE,
    SEPARATION,
    COHESION,
    RANGE,
)

shapes.Triangle._anchor_y = -BOID_SIZE

class Boid:
    def __init__(self, x, y, vx, vy, color, batch):
        self.shape = shapes.Triangle(
            x, y + BOID_SIZE,
            x - BOID_SIZE, y - BOID_SIZE,
            x + BOID_SIZE, y - BOID_SIZE,
            color=color,
            batch=batch
        )
        self.vx = vx
        self.vy = vy

    def wrap_around(self, gap, hue):
        if self.shape.x > WINDOW_WIDTH + gap:
            self.shape.x = 0 - gap
            self.shape.color = (255, 0, hue)
        elif self.shape.x < 0 - gap:
            self.shape.x = WINDOW_WIDTH + gap
            self.shape.color = (255, 0, hue)

        if self.shape.y > WINDOW_HEIGHT + gap:
            self.shape.y = 0 - gap
            self.shape.color = (255, 0, hue)
        elif self.shape.y < 0 - gap:
            self.shape.y = WINDOW_HEIGHT + gap
            self.shape.color = (255, 0, hue)

    def steer(self, target_vx, target_vy, factor):
        self.vx += factor * (target_vx)
        self.vy += factor * (target_vy)

    def stabalize_vel(self):
        velocity = math.sqrt(self.vx**2 + self.vy**2)
        if velocity == 0:
            target_vx = random.uniform(0.1, BOID_SPEED)
            target_vy = random.uniform(0.1, BOID_SPEED)
        else:
            target_vx = (self.vx / velocity) * BOID_SPEED
            target_vy = (self.vy / velocity) * BOID_SPEED

        self.steer(target_vx - self.vx, target_vy - self.vy, 0.2)

    def calculate_vel(self, boids, predators):
        ct = 0
        sum_x = 0
        sum_y = 0
        sum_vx = 0
        sum_vy = 0
        for other in boids:
            if other is self:
                continue
            dst_x = other.shape.x - self.shape.x
            dst_y = other.shape.y - self.shape.y
            dst = math.sqrt((dst_x)**2 + (dst_y)**2)
            if dst < RANGE and dst > 0:
                push_vx = -dst_x / dst**1.4
                push_vy = -dst_y / dst**1.4
                self.steer(push_vx, push_vy, SEPARATION)
                sum_x += dst_x 
                sum_y += dst_y 
                sum_vx += other.vx - self.vx
                sum_vy += other.vy - self.vy
                ct += 1
        if ct > 0:
            self.steer(sum_x/ct, sum_y/ct, COHESION)
            self.steer(sum_vx/ct, sum_vy/ct, ALIGNMENT)

        for predator in predators:
            dst_x = predator.shape.x - self.shape.x
            dst_y = predator.shape.y - self.shape.y
            dst = math.sqrt((dst_x)**2 + (dst_y)**2)
            if dst < RANGE and dst > 0:
                push_vx = -dst_x / dst**1.4
                push_vy = -dst_y / dst**1.4
                self.steer(push_vx, push_vy, SEPARATION * 8)

    def update(self, dt, boids, predators, hue):
        self.stabalize_vel()
        self.calculate_vel(boids, predators)
 
        self.shape.x += self.vx * dt
        self.shape.y += self.vy * dt
        self.wrap_around(BOID_SIZE, hue)
        self.shape.rotation = -math.degrees(math.atan2(self.vy, self.vx)) + 90


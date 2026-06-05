import math
import random
from pyglet import shapes
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BOID_SPEED,
    BOID_SIZE,
    BOID_COLOR,
    SEPARATION,
    RANGE,
)

shapes.Triangle._anchor_y = -BOID_SIZE

class Boid:
    def __init__(self, x, y, vx, vy, batch):
        self.shape = shapes.Triangle(
            x, y + BOID_SIZE,
            x - BOID_SIZE, y - BOID_SIZE,
            x + BOID_SIZE, y - BOID_SIZE,
            color=BOID_COLOR,
            batch=batch
        )
        self.vx = vx
        self.vy = vy

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
    
    def separation(self, other, dst):
        push_vx = self.shape.x - other.shape.x
        push_vy = self.shape.y - other.shape.y
        push_vx /= dst**1.4
        push_vy /= dst**1.4
        self.steer(push_vx, push_vy, SEPARATION)
 
    def update(self, dt, boids):
        velocity = math.sqrt(self.vx**2 + self.vy**2)
        if velocity == 0:
            target_vx = random.uniform(0.1, BOID_SPEED)
            target_vy = random.uniform(0.1, BOID_SPEED)
        else:
            target_vx = (self.vx / velocity) * BOID_SPEED
            target_vy = (self.vy / velocity) * BOID_SPEED

        self.vx += 0.2 * (target_vx - self.vx)
        self.vy += 0.2 * (target_vy - self.vy)
 
        for other in boids:
            if other is self:
                continue
            dst = math.sqrt((self.shape.x - other.shape.x)**2 + (self.shape.y - other.shape.y)**2)
            if dst < RANGE and dst > 0:
                self.separation(other, dst)
 
        self.shape.x += self.vx * dt
        self.shape.y += self.vy * dt
 
        self.wrap_around(BOID_SIZE)

        self.shape.rotation = -math.degrees(math.atan2(self.vy, self.vx)) + 90


import math
from pyglet import shapes
from constants import BOID_SIZE, BOID_COLOR, BOID_SPEED, WINDOW_HEIGHT, WINDOW_WIDTH

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
        self.vx += factor * (target_vx - self.vx)
        self.vy += factor * (target_vy - self.vy)
        
    def update(self, dt):
        distance = math.sqrt(self.vx**2 + self.vy**2)
        if distance == 0:
            distance = 0.01
        target_vx = (self.vx / distance) * BOID_SPEED
        target_vy = (self.vy / distance) * BOID_SPEED

        self.steer(target_vx, target_vy, 0.02)

        self.shape.x += self.vx * dt
        self.shape.y += self.vy * dt

        self.wrap_around(BOID_SIZE)

        self.shape.rotation = -math.degrees(math.atan2(self.vy, self.vx)) + 90

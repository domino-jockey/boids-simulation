import random
import math
import pyglet
from pyglet import shapes
from pyglet.window import key

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Boids Simulation"
FPS = 60
NUM_BOIDS = 5
BOID_COLOR = (245, 95, 95)
BOID_SPEED = 200
BOID_SIZE = 15

# Setup
pyglet.options["dpi_scaling"] = "real"

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption=WINDOW_TITLE)
keys = key.KeyStateHandler()
window.push_handlers(keys)
batch = pyglet.graphics.Batch()
debug_label = pyglet.text.Label(
    text="FPS: 0",
    font_name='Arial',
    font_size=32,
    x=WINDOW_WIDTH // 2,
    y=WINDOW_HEIGHT - 50,
    anchor_x='center',
    anchor_y='center',
    batch=batch
)


class Boid:
    def __init__(self, x, y, vx, vy):
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

class Simulation:
    def __init__(self):
        shapes.Triangle._anchor_y = -BOID_SIZE
        self.boids = []
        for _ in range(NUM_BOIDS):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.boids.append(Boid(x, y, random.uniform(-1, 1), random.uniform(-1, 1)))

    def update(self, dt):
        debug_label.text = f"FPS: {1/dt:.0f}"
        for boid in self.boids:
            boid.update(dt)

    def draw(self):
        window.clear()
        batch.draw()

sim = Simulation()

@window.event
def on_draw():
    sim.draw()

pyglet.clock.schedule_interval(sim.update, 1/FPS)
pyglet.app.run()

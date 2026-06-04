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
NUM_BOIDS = 20
BOID_COLOR = (245, 95, 95)

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

BOID_SPEED = 100

class Boid:
    def __init__(self, x, y, vx, vy):
        self.shape = shapes.Triangle(
            x, y + 15,
            x - 15, y - 15,
            x + 15, y - 15,
            color=BOID_COLOR,
            batch=batch
        )
        self.vx = vx
        self.vy = vy

    def update(self, dt):
        self.shape.x += self.vx * dt
        self.shape.y += self.vy * dt

        if self.shape.x > WINDOW_WIDTH:
            self.shape.x = 0
        elif self.shape.x < 0:
            self.shape.x = WINDOW_WIDTH

        if self.shape.y > WINDOW_HEIGHT:
            self.shape.y = 0
        elif self.shape.y < 0:
            self.shape.y = WINDOW_HEIGHT

        self.shape.rotation = -math.degrees(math.atan2(self.vy, self.vx)) + 90

class Simulation:
    def __init__(self):
        shapes.Triangle._anchor_x = 15
        shapes.Triangle._anchor_y = 15
        self.boids = []
        for _ in range(NUM_BOIDS):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            angle = random.uniform(0, 2 * math.pi)
            self.boids.append(Boid(x, y, BOID_SPEED * math.cos(angle), BOID_SPEED * math.sin(angle)))

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

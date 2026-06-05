import random
import pyglet
from pyglet.window import key
from boid import Boid
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    NUM_BOIDS,
    FPS
)

# Setup
pyglet.options["dpi_scaling"] = "real"

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption=WINDOW_TITLE)
keys = key.KeyStateHandler()
window.push_handlers(keys)

batch = pyglet.graphics.Batch()

class Simulation:
    def __init__(self):
        self.boids = []
        for _ in range(NUM_BOIDS):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.boids.append(Boid(x, y, random.uniform(-1, 1), random.uniform(-1, 1), batch))

    def update(self, dt):
        for boid in self.boids:
            boid.update(dt, self.boids)

    def draw(self):
        pyglet.shapes.Rectangle(0, 0, window.width, window.height, color=(0, 0, 0, 60)).draw()
        batch.draw()

sim = Simulation()

@window.event
def on_draw():
    sim.draw()

pyglet.clock.schedule_interval(sim.update, 1/FPS)
pyglet.app.run()

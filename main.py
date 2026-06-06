import random
import pyglet
from pyglet.window import key
from boid import Boid
from predator import Predator
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    NUM_BOIDS,
    NUM_PREDATORS,
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
        self.predators = []
        self.hue = 0
        self.hue_ct = 0
        for _ in range(NUM_BOIDS):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            color = int(y / WINDOW_HEIGHT * 255)
            self.boids.append(Boid(x, y, random.uniform(-1, 1), random.uniform(-1, 1), (255, 0, color), batch))
        for _ in range(NUM_PREDATORS):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.predators.append(Predator(x, y, batch))

    def change_hue(self):
        self.hue_ct += 1
        self.hue_ct %= 511
        if self.hue_ct < 256:
            self.hue = self.hue_ct
        else:
            self.hue = 510 - self.hue_ct

    def update(self, dt):
        self.change_hue()
        for boid in self.boids:
            boid.update(dt, self.boids, self.predators, self.hue)
        for predator in self.predators:
            predator.update(dt, self.boids)

    def draw(self):
        pyglet.shapes.Rectangle(0, 0, window.width, window.height, color=(0, 0, 0, 60)).draw()
        batch.draw()

sim = Simulation()

@window.event
def on_draw():
    sim.draw()

pyglet.clock.schedule_interval(sim.update, 1/FPS)
pyglet.app.run()

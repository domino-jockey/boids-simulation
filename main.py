import random
import pyglet
from pyglet import shapes
from pyglet.window import key
from boid import Boid
from constants import BOID_SIZE, NUM_BOIDS, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH, FPS

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

class Simulation:
    def __init__(self):
        shapes.Triangle._anchor_y = -BOID_SIZE
        self.boids = []
        for _ in range(NUM_BOIDS):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.boids.append(Boid(x, y, random.uniform(-1, 1), random.uniform(-1, 1), batch))

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

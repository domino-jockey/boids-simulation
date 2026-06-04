import random
import pyglet
from pyglet import shapes
from pyglet.window import key

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
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

class Simulation:
    def __init__(self):
        shapes.Triangle._anchor_x = 15
        shapes.Triangle._anchor_y = 15
        self.boids = []
        for _ in range(NUM_BOIDS):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            t = shapes.Triangle(
                x, y + 15,
                x - 15, y - 15,
                x + 15, y - 15,
                color=BOID_COLOR,
                batch=batch
            )
            self.boids.append(t)

    def update(self, dt):
        debug_label.text = f"FPS: {1/dt:.0f}"

    def draw(self):
        window.clear()
        batch.draw()

sim = Simulation()

@window.event
def on_draw():
    sim.draw()

pyglet.clock.schedule_interval(sim.update, 1/FPS)
pyglet.app.run()

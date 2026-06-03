import pyglet
from pyglet.window import key

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Boids Simulaiton"
FPS = 60
GRAVITY = -1800
GROUND_Y = 300

# Setup
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption=WINDOW_TITLE)
keys = key.KeyStateHandler()
window.push_handlers(keys)
batch = pyglet.graphics.Batch()

debug_label = pyglet.text.Label(
    text=f"Score: 0",
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
        pass

    def update(self, dt):
        pass

    def draw(self):
        window.clear()
        batch.draw()

sim = Simulation()

@window.event
def on_draw():
    sim.draw()

pyglet.clock.schedule_interval(sim.update, 1/FPS)
pyglet.app.run()

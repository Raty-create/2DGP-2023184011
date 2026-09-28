import math
from pico2d import *

# stage setup
VIEW_W, VIEW_H = 800, 600
hub_x, hub_y = VIEW_W // 2, VIEW_H // 2
reach = 200
steps_per_lap = 360
stride = 0.01
breather = 0.5

open_canvas(VIEW_W, VIEW_H)
sprite = load_image('character.png')

alive = True


class CircleRoute:
    """Position on a ring, driven by a 0.0 - 1.0 progress value."""

    def __init__(self, tag, ox, oy, radius):
        self.tag = tag
        self.ox, self.oy, self.radius = ox, oy, radius

    def sample(self, progress):
        turn = math.tau * (progress % 1.0)
        return (self.ox + self.radius * math.cos(turn),
                self.oy + self.radius * math.sin(turn))


class PolygonRoute:
    """Closed polyline walked at a constant speed along its perimeter."""

    def __init__(self, tag, corners):
        self.tag = tag
        self.legs = []

        walked = 0.0
        for i, (ax, ay) in enumerate(corners):
            bx, by = corners[(i + 1) % len(corners)]
            length = math.hypot(bx - ax, by - ay)
            self.legs.append((ax, ay, bx, by, walked, walked + length))
            walked += length

        self.perimeter = walked

    def sample(self, progress):
        target = (progress % 1.0) * self.perimeter

        for ax, ay, bx, by, near, far in self.legs:
            if target <= far:
                ratio = (target - near) / (far - near)
                return (ax + (bx - ax) * ratio, ay + (by - ay) * ratio)

        return self.legs[-1][2], self.legs[-1][3]


def quit_pressed():
    for e in get_events():
        if e.type == SDL_QUIT:
            return True
        if e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
            return True
    return False


def stamp(x, y):
    clear_canvas()
    sprite.draw(x, y)
    update_canvas()
    delay(stride)


def lap(route):
    for tick in range(steps_per_lap):
        if quit_pressed():
            return False

        x, y = route.sample(tick / steps_per_lap)
        stamp(x, y)

    return True


program = [
    CircleRoute('CIRCLE', hub_x, hub_y, reach),
    PolygonRoute('SQUARE', [
        (hub_x - reach, hub_y + reach),
        (hub_x + reach, hub_y + reach),
        (hub_x + reach, hub_y - reach),
        (hub_x - reach, hub_y - reach),
    ]),
    PolygonRoute('TRIANGLE', [
        (hub_x, hub_y + reach),
        (hub_x + reach, hub_y - reach),
        (hub_x - reach, hub_y - reach),
    ]),
]

while alive:
    for route in program:
        print(route.tag)

        if not lap(route):
            alive = False
            break

        delay(breather)

close_canvas()

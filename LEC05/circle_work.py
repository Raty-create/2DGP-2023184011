## 여기를 채우시오.
from pico2d import *
import math

PI = 3.14159
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)

# grass = load_image('grass.png')
character = load_image('character.png')

class GameCharacter:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.draw = character.draw

character = GameCharacter()

def game_is_running():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            return False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True

def render_game_state():
    cx = WINDOW_WIDTH // 2
    cy = WINDOW_HEIGHT // 2
    radius = 100
    angle = 0

    while angle < 360:
        clear_canvas()
        radian = angle * PI / 180
        character.x = cx + radius * math.cos(radian)
        character.y = cy + radius * math.sin(radian)
        angle += 2
        character.draw(character.x, character.y)
        update_canvas()
        delay(0.011)

while game_is_running():
    render_game_state()

close_canvas()
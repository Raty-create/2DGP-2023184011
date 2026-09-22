## 여기를 채우시오.
from pico2d import *

open_canvas(800, 600)

# grass = load_image('grass.png')
character = load_image('character.png')

class GameCharacter:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.dir = 0
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
    clear_canvas()

    if character.dir == 0:
        character.draw(character.x, character.y)
        character.x += 2
        if character.x >= 400:
            character.x = 400
            character.dir = 1
        delay(0.01)
    elif character.dir == 1:
        character.draw(character.x, character.y)
        character.y += 2
        if character.y >= 400:
            character.y = 400
            character.dir = 2
        delay(0.01)
    elif character.dir == 2:
        character.draw(character.x, character.y)
        character.x -= 2
        if character.x <= 50:
            character.x = 50
            character.dir = 3
        delay(0.01)
    elif character.dir == 3:
        character.draw(character.x, character.y)
        character.y -= 2
        if character.y <= 50:
            character.y = 50
            character.dir = 0
        delay(0.01)

while game_is_running():
    update_canvas()
    render_game_state()

close_canvas()
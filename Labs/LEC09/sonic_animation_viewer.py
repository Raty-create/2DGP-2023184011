from pico2d import *

# 뷰어를 그릴 캔버스의 크기. LEC08의 animation_viewer.py와 같은 해상도를 쓴다.
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

running = True

while running:
    clear_canvas()

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    update_canvas()

close_canvas()
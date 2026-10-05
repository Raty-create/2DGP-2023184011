from pico2d import *

# 뷰어를 그릴 캔버스의 크기. LEC08의 animation_viewer.py와 같은 해상도를 쓴다.
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

# 뷰어가 재생할 스프라이트 시트. 뷰어와 같은 폴더에 둔다.
SPRITE_SHEET_FILE = "sonic-sprite.png"

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

# 알파 채널이 있는 투명 배경 시트이므로 캔버스만 지우면 된다.
# LEC08이 알파 없는 RGB 시트 때문에 쓰던 배경색 덮어쓰기는 필요 없다.
sheet = load_image(SPRITE_SHEET_FILE)

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
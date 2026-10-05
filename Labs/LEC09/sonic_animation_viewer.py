from pico2d import *

# 뷰어가 그릴 캔버스의 크기. LEC08의 animation_viewer.py와 같은 해상도를 쓴다.
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

# 뷰어가 재생할 스프라이트 시트. 뷰어와 같은 폴더에 둔다.
SPRITE_SHEET_FILE = "sonic-sprite.png"

# 원본 프레임 최대 높이는 45px다. 45 * 4 = 180px로 확대하면 600px 높이 화면의
# 삼분의 1을 차지해 동작 자세가 선명하게 보인다. 더 크게 하면 잘려 나간다.
CHARACTER_SCALE = 4

# 한 프레임을 화면에 보여 주는 시간이다. 1 / 0.08 = 12.5fps.
# 프레임이 4개짜리 액션은 0.32초, 12개짜리 액션은 0.96초가 되어
# 어느 액션도 너무 빠르지도 느리지도 않은 박자에 들어간다.
FRAME_DURATION = 0.08

# 한 액션을 몇 번 반복한 뒤 다음 액션으로 넘어갈지 정한다.
REPEAT_COUNT = 5

# REPEAT_COUNT회 반복이 끝난 뒤 다음 액션으로 넘어가기 전에 멈춰 있는 시간이다.
PAUSE_TIME = 1.0

# 캐릭터가 서 있는 바닥선. 프레임마다 높이가 다르므로
# 프레임의 아래쪽 끝을 이 기준선에 맞춰 그린다.
# 최대 표시 높이 180px를 감안해 화면 중앙(300)보다 아래에 둔다.
GROUND_Y = 380

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
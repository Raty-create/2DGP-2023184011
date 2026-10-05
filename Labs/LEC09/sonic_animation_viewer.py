from pico2d import *
from collections import namedtuple

# 한 프레임 = 스프라이트 시트 안의 사각형 영역.
# left, bottom은 사각형의 왼쪽 위 좌표, width, height는 잘라낼 크기이다.
Frame = namedtuple("Frame", "left bottom width height")

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

# 뷰어가 무엇을 재생하는지 시작하자마자 확인하게 해준다.
print("sprite sheet loaded: %d x %d" % (sheet.w, sheet.h))

# Idle: 시트에서 첫 번째 액션 행(bottom = 77). 11프레임.
# sonic 시트는 균일 격자가 아니라 행마다 프레임 크기가 다른 밀집 배치라
# (열, 행) 계산으로는 프레임을 얻을 수 없다. 좌표를 직접 재야 한다.
# 액션 안에서 bottom을 77로 통일한 것은, 프레임마다 실제 높이가 다른데
# 아래쪽 끝을 맞추지 않으면 캐릭터가 위아래로 흔들리기 때문이다.
IDLE_FRAMES = [
    Frame(  1, 77, 29, 39), Frame( 31, 77, 26, 38), Frame( 58, 77, 28, 39),
    Frame( 86, 77, 30, 38), Frame(118, 77, 30, 38), Frame(150, 77, 30, 38),
    Frame(182, 77, 29, 38), Frame(211, 77, 29, 39), Frame(240, 77, 29, 39),
    Frame(270, 77, 24, 33), Frame(302, 77, 29, 27),
]

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
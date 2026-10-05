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

# Walk: 시트 두 번째 액션 행(bottom = 117). 12프레임.
# 이 행은 시트 전체 폭(399px)을 끝까지 쓴다. 마지막 2프레임(x >= 334)은
# 다른 행에서 쓰지 않는 우측 영역에 있지만 Idle의 뒤 2프레임과 마찬가지로
# 이 액션의 연속 프레임으로 본다.
WALK_FRAMES = [
    Frame(  8, 117, 26, 38), Frame( 37, 117, 27, 38), Frame( 65, 117, 31, 38),
    Frame( 97, 117, 37, 38), Frame(135, 117, 32, 38), Frame(170, 117, 32, 39),
    Frame(206, 117, 26, 39), Frame(238, 117, 24, 38), Frame(263, 117, 30, 38),
    Frame(295, 117, 36, 38), Frame(334, 117, 32, 38), Frame(370, 117, 29, 39),
]

# Run: 시트 세 번째 액션 행(bottom = 163). 6프레임.
RUN_FRAMES = [
    Frame(  1, 163, 33, 40), Frame( 39, 163, 35, 40), Frame( 89, 163, 35, 39),
    Frame(130, 163, 34, 43), Frame(181, 163, 34, 42), Frame(228, 163, 33, 42),
]

# Dash: 시트 네 번째 액션 행(bottom = 199). 9프레임.
DASH_FRAMES = [
    Frame(  1, 199, 29, 31), Frame( 36, 199, 28, 33), Frame( 67, 199, 30, 31),
    Frame( 98, 199, 31, 30), Frame(131, 199, 29, 32), Frame(162, 199, 29, 32),
    Frame(193, 199, 30, 30), Frame(230, 199, 31, 30), Frame(268, 199, 30, 30),
]

# LookUp: 시트 다섯 번째 액션 행(bottom = 232). 6프레임.
# 시트 전체에서 높이가 가장 낮은 행(27px)이다.
LOOK_UP_FRAMES = [
    Frame(  1, 232, 30, 27), Frame( 36, 232, 29, 27), Frame( 70, 232, 29, 27),
    Frame(105, 232, 29, 27), Frame(139, 232, 29, 27), Frame(174, 232, 29, 27),
]

# Crouch: 시트 여섯 번째 액션 행(bottom = 273). 6프레임.
CROUCH_FRAMES = [
    Frame(  1, 273, 29, 35), Frame( 36, 273, 30, 35), Frame( 74, 273, 31, 35),
    Frame(111, 273, 31, 36), Frame(149, 273, 30, 35), Frame(186, 273, 31, 36),
]

# Roll: 시트 일곱 번째 액션 행(bottom = 317). 6프레임.
# 앞 2프레임은 폭이 29~30px, 뒤 4프레임은 38~39px로 넓다.
# 구르는 동안 몸이 길어지는 모양이 그대로 담겨 있는 행이다.
ROLL_FRAMES = [
    Frame(  1, 317, 29, 35), Frame( 36, 317, 30, 35), Frame( 72, 317, 39, 32),
    Frame(123, 317, 39, 33), Frame(172, 317, 39, 32), Frame(218, 317, 38, 33),
]

# Push: 시트 여덟 번째 액션 행(bottom = 370). 8프레임.
# 시트에서 높이가 가장 큰 행(45px)이다. 뒤 2프레임은 실제로는 30px 높이에
# 아래쪽에 놓여 있으므로, 위쪽 빈 영역까지 포함한 45px 높이로 잘라야
# 다른 프레임과 발의 높이가 맞는다.
PUSH_FRAMES = [
    Frame(  1, 370, 24, 45), Frame( 31, 370, 29, 44), Frame( 65, 370, 20, 44),
    Frame( 90, 370, 25, 44), Frame(119, 370, 25, 44), Frame(149, 370, 20, 44),
    Frame(184, 370, 40, 30), Frame(232, 370, 39, 30),
]

# Hurt: 시트 아홉 번째 액션 행(bottom = 416). 8프레임.
HURT_FRAMES = [
    Frame(  1, 416, 27, 38), Frame( 31, 416, 31, 38), Frame( 64, 416, 31, 38),
    Frame( 99, 416, 33, 40), Frame(136, 416, 32, 38), Frame(176, 416, 33, 38),
    Frame(217, 416, 33, 38), Frame(254, 416, 33, 39),
]

# Death: 시트 열 번째 액션 행(bottom = 468). 4프레임.
# 프레임이 4개뿐인 가장 짧은 행이다. 12.5fps로 돌면 사이클이 0.32초라
# 성급하게 느껴질 수 있어, 실제 재생 화면을 보고 조정 대상으로 남겨 둔다.
DEATH_FRAMES = [
    Frame(  6, 468, 34, 40), Frame( 49, 468, 34, 43), Frame( 96, 468, 23, 42),
    Frame(125, 468, 23, 42),
]

# SPRITE = (action 이름, 그 action의 frame tuple)들의 나열.
# 이 순서가 화면에 재생되는 순서이며, 마지막 다음에는 첫 번째로 돌아간다.
# 여기를 고치면 액션 추가·삭제만으로 목록이 바뀌고 재생 로직은 손대지 않아도 된다.
SPRITE = [
    ("Idle", IDLE_FRAMES),
    ("Walk", WALK_FRAMES),
    ("Run", RUN_FRAMES),
    ("Dash", DASH_FRAMES),
    ("LookUp", LOOK_UP_FRAMES),
    ("Crouch", CROUCH_FRAMES),
    ("Roll", ROLL_FRAMES),
    ("Push", PUSH_FRAMES),
    ("Hurt", HURT_FRAMES),
    ("Death", DEATH_FRAMES),
]

for name, frames in SPRITE:
    print("%-12s : %2d frames" % (name, len(frames)))


def draw_frame(frame, x, y, scale=1.0):
    # 앞의 네 값은 스프라이트 시트 안의 프레임 영역, 뒤의 두 값은 캔버스 좌표이다.
    # 마지막 두 값은 화면에 표시할 크기이므로, 잘라내는 크기와 배율을 분리할 수 있다.
    sheet.clip_draw(frame.left, frame.bottom,
                    frame.width, frame.height,
                    x, y, frame.width * scale, frame.height * scale)

running = True

while running:
    clear_canvas()

    # 프레임 좌표가 맞는지 확인하려면 한 프레임만 그려 보면 된다.
    # 일단 Idle의 첫 프레임을 원본 크기 그대로 화면 중앙에 둔다.
    draw_frame(IDLE_FRAMES[0], CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    update_canvas()

close_canvas()
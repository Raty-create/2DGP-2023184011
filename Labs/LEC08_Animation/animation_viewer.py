from pico2d import *
from collections import namedtuple

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

SPRITE_SHEET_FILE = "Mario_sprite_sheet.png"
SHEET_WIDTH = 500
SHEET_HEIGHT = 190

# 원본 스프라이트는 34px 정도로 작으므로 9배로 확대한다.
# 34 * 9 = 306px로, 600px 높이 화면의 절반을 차지한다.
CHARACTER_SCALE = 9

# 프레임 하나를 화면에 보여 주는 시간이다. 짧으면 빠르고 길면 끊겨 보인다.
FRAME_DURATION = 0.08

# 한 action을 몇 번 반복한 뒤 다음 action으로 넘어갈지 정한다.
REPEAT_COUNT = 5

# 5회 반복이 끝난 뒤 다음 action으로 넘어가기 전에 멈춰 있는 시간이다.
PAUSE_TIME = 1.0

# 한 프레임 = 스프라이트 시트 안의 사각형 영역.
# left, bottom은 사각형의 왼쪽 아래 좌표, width, height는 잘라낼 크기이다.
Frame = namedtuple("Frame", "left bottom width height")

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
character = load_image(SPRITE_SHEET_FILE)

print("sprite sheet loaded: %d x %d" % (character.w, character.h))

# MovingIdle: 시트 첫 번째 줄(bottom = 145). 6프레임 걷기 사이클이 두 번 반복된 12프레임.
MOVING_IDLE_FRAMES = [
    Frame(  8, 145, 18, 34), Frame( 31, 145, 18, 34),
    Frame( 54, 145, 20, 33), Frame( 79, 145, 23, 32),
    Frame(107, 145, 20, 33), Frame(132, 145, 18, 34),
    Frame(155, 145, 18, 34), Frame(178, 145, 18, 34),
    Frame(201, 145, 20, 33), Frame(226, 145, 23, 32),
    Frame(254, 145, 20, 33), Frame(279, 145, 18, 34),
]

# VictoryPose: 시트 두 번째 줄. MovingIdle과 프레임 수가 다른 5프레임.
VICTORY_POSE_FRAMES = [
    Frame(  8, 103, 20, 34), Frame( 33, 103, 22, 33),
    Frame( 60, 103, 23, 32), Frame( 88, 103, 22, 33),
    Frame(119, 104, 22, 32),
]

# FallAndRoll: 시트 세 번째 줄. 16프레임.
# 0~7은 넘어지고 일어나는 구간, 8~15는 4프레임 구름 동작이 두 번 반복된 구간이다.
FALL_AND_ROLL_FRAMES = [
    Frame(  8,  62, 20, 27), Frame( 47,  61, 21, 27),
    Frame( 80,  55, 27, 27), Frame(112,  55, 29, 27),
    Frame(148,  55, 22, 33), Frame(175,  55, 27, 31),
    Frame(209,  56, 23, 33), Frame(237,  56, 23, 27),
    Frame(265,  56, 16, 29), Frame(286,  56, 24, 26),
    Frame(315,  56, 29, 16), Frame(349,  56, 26, 24),
    Frame(380,  56, 16, 29), Frame(401,  56, 24, 26),
    Frame(430,  56, 29, 16), Frame(464,  56, 26, 24),
]

# TurnInPlace: 시트 네 번째 줄. 4프레임 회전이 두 번 반복된 8프레임.
TURN_IN_PLACE_FRAMES = [
    Frame(  8,   7, 18, 34), Frame( 31,   7, 16, 34),
    Frame( 52,   7, 17, 34), Frame( 74,   7, 16, 34),
    Frame( 95,   7, 18, 34), Frame(118,   7, 16, 34),
    Frame(139,   7, 17, 34), Frame(161,   7, 16, 34),
]

# SPRITE = (action 이름, 그 action의 frame tuple)들의 나열.
SPRITE = [
    ("MovingIdle", MOVING_IDLE_FRAMES),
    ("VictoryPose", VICTORY_POSE_FRAMES),
    ("FallAndRoll", FALL_AND_ROLL_FRAMES),
    ("TurnInPlace", TURN_IN_PLACE_FRAMES),
]

for name, frames in SPRITE:
    print("%-12s : %2d frames" % (name, len(frames)))


def screen_center():
    return CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2


# action마다 독립적으로 진행되는 재생 상태를 만들어 둔다.
def create_state():
    return {
        "frame": 0,
        "frame_elapsed": 0.0,
        "repeat": 0,
        "done": False,
        "pause_elapsed": 0.0,
        "last_time": get_time(),
    }


ANIMATION_STATES = [create_state() for _ in SPRITE]

# 지금 재생 중인 action의 SPRITE 안에서의 번호.
current_action = 0
current_finished = False


def draw_frame(frame, x, y, scale=1.0):
    # 앞의 네 값은 스프라이트 시트 안의 프레임 영역, 뒤의 두 값은 캔버스 좌표이다.
    # 마지막 두 값은 화면에 표시할 크기이므로, 잘라내는 크기와 배율을 분리할 수 있다.
    character.clip_draw(frame.left, frame.bottom,
                        frame.width, frame.height,
                        x, y, frame.width * scale, frame.height * scale)


# 클립 하나를 진행시키고 화면에 그리는 공통 재생기.
def play_clip(frames, state, action):
    global current_finished

    if action != current_action:
        return

    now = get_time()
    delta = now - state["last_time"]
    state["last_time"] = now
    state["frame_elapsed"] += delta

    if state["done"]:
        state["pause_elapsed"] += delta
        if state["pause_elapsed"] >= PAUSE_TIME:
            state["done"] = False
            state["pause_elapsed"] = 0.0
            state["repeat"] = 0
            # 5회 반복과 정지가 끝났음을 알린다.
            current_finished = True
    elif state["frame_elapsed"] >= FRAME_DURATION:
        state["frame_elapsed"] -= FRAME_DURATION
        if state["frame"] < len(frames) - 1:
            state["frame"] += 1
        else:
            state["frame"] = 0
            state["repeat"] += 1
            if state["repeat"] >= REPEAT_COUNT:
                state["done"] = True
                # 정지 중에는 마지막 프레임을 유지한다.
                state["frame"] = len(frames) - 1

    x, y = screen_center()
    draw_frame(frames[state["frame"]], x, y, CHARACTER_SCALE)


def MovingIdle():
    play_clip(MOVING_IDLE_FRAMES, ANIMATION_STATES[0], 0)

def VictoryPose():
    play_clip(VICTORY_POSE_FRAMES, ANIMATION_STATES[1], 1)

def FallAndRoll():
    play_clip(FALL_AND_ROLL_FRAMES, ANIMATION_STATES[2], 2)

def TurnInPlace():
    play_clip(TURN_IN_PLACE_FRAMES, ANIMATION_STATES[3], 3)


# 현재 action의 재생을 끝내고 다음 action으로 넘어간다.
# 마지막 action 다음에는 0번으로 돌아가므로 전체 목록이 무한 반복된다.
def select_next_action():
    global current_action, current_finished

    if not current_finished:
        return
    current_finished = False

    current_action = (current_action + 1) % len(SPRITE)
    state = ANIMATION_STATES[current_action]
    state["frame"] = 0
    state["repeat"] = 0
    state["last_time"] = get_time()

while True:
    clear_canvas()
    MovingIdle()
    VictoryPose()
    FallAndRoll()
    TurnInPlace()
    select_next_action()
    update_canvas()

close_canvas()
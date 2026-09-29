from pico2d import *
from collections import namedtuple

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

SPRITE_SHEET_FILE = "Mario_sprite_sheet.png"
SHEET_WIDTH = 500
SHEET_HEIGHT = 190

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

def MovingIdle():
    pass

def VictoryPose():
    pass

def FallAndRoll():
    pass

def TurnInPlace():
    pass

while True:
    clear_canvas()
    MovingIdle()
    VictoryPose()
    FallAndRoll()
    TurnInPlace()
    update_canvas()

close_canvas()
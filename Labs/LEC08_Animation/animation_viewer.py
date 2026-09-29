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
from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
character = load_image("Mario_sprite_sheet.png")

def MovingIdle():
    pass

def VictoryPose():
    pass

def FallAndRoll():
    pass

def TurnInPlace():
    pass

while True:
    MovingIdle()
    VictoryPose()
    FallAndRoll()
    TurnInPlace()
    pass

close_canvas()
from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

SPRITE_SHEET_FILE = "Mario_sprite_sheet.png"
SHEET_WIDTH = 500
SHEET_HEIGHT = 190

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
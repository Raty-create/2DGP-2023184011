#실습 과제 진행
from pico2d import *
import math

# 맨처음 해야 할 일은.
open_canvas(800, 600)
character = load_image('character.png')

# 애니메이션 속도 조절용 상수
X_FRAME = 0.01

def move_circle():
    print("CIRCLE")
    # 캐릭터 이미지 표시
    clear_canvas()
    character.draw(400, 300)
    update_canvas()
    pass

def move_rectangle():
    print("RECTANGLE")
    pass

def move_triangle():
    print("TRIANGLE")
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    delay(X_FRAME)

close_canvas()
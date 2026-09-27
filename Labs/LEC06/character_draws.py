#실습 과제 진행
from pico2d import *
import math

# 맨처음 해야 할 일은.
open_canvas(800, 600)
character = load_image('character.png')

# 캐릭터가 도는 화면 중앙 좌표
CENTER_X = 400
CENTER_Y = 300

# 원 궤적의 반지름
RADIUS = 200

# 애니메이션 속도 조절용 상수
X_FRAME = 0.01

def move_circle():
    print("CIRCLE")
    # 캐릭터 이미지 표시
    clear_canvas()
    character.draw(CENTER_X, CENTER_Y)
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
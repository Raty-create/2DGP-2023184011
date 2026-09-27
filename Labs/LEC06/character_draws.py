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

# 사각형 궤적의 가로 / 세로 길이
RECT_W = 400
RECT_H = 400

# 애니메이션 속도 조절용 상수
X_FRAME = 0.01

def move_circle():
    print("CIRCLE")

    degree = 0
    while True:
        # 캐릭터 이미지 표시
        clear_canvas()

        theta = math.radians(degree)

        # 코사인 값으로 x 좌표 계산
        x = CENTER_X + RADIUS * math.cos(theta)

        # 사인 값으로 y 좌표 계산
        y = CENTER_Y + RADIUS * math.sin(theta)

        character.draw(x, y)
        update_canvas()
        delay(X_FRAME)

        # 한 바퀴(360도)를 돌면 다시 0도로 돌아간다
        degree += 1
        if degree == 360:
            degree = 0

def move_rectangle():
    print("RECTANGLE")

    # 사각형 궤적의 네 변 좌표
    left = CENTER_X - RECT_W / 2
    right = CENTER_X + RECT_W / 2
    top = CENTER_Y - RECT_H / 2
    bottom = CENTER_Y + RECT_H / 2

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
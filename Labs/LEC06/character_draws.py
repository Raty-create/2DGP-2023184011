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

# 한 바퀴를 도는 프레임 수를 원운동(360프레임 = 3.6초)에 맞춘다
# 사각형: 4변 x (스텝 + 1) = 360  ->  스텝 89
# 삼각형: 3변 x (스텝 + 1) = 360  ->  스텝 119
RECT_STEPS = 89
TRI_STEPS = 119

# 삼각형 꼭짓점 좌표 (위쪽, 오른쪽 아래, 왼쪽 아래)
TRI_TOP = (CENTER_X, CENTER_Y + RADIUS)
TRI_RIGHT = (CENTER_X + RADIUS, CENTER_Y - RADIUS)
TRI_LEFT = (CENTER_X - RADIUS, CENTER_Y - RADIUS)

# 애니메이션 속도 조절용 상수
X_FRAME = 0.01

# 도형이 바뀔 때 잠깐 멈추는 시간
PAUSE = 0.5

# 한 프레임에 캐릭터 한 장을 그리는 함수
def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(X_FRAME)

def move_circle():
    print("CIRCLE")

    degree = 0
    while degree < 360:
        theta = math.radians(degree)

        # 코사인 값으로 x 좌표 계산
        x = CENTER_X + RADIUS * math.cos(theta)

        # 사인 값으로 y 좌표 계산
        y = CENTER_Y + RADIUS * math.sin(theta)

        # 캐릭터 이미지 표시
        draw_character(x, y)

        degree += 1

def move_rectangle():
    print("RECTANGLE")

    # 사각형 궤적의 네 변 좌표
    left = CENTER_X - RECT_W / 2
    right = CENTER_X + RECT_W / 2
    top = CENTER_Y - RECT_H / 2
    bottom = CENTER_Y + RECT_H / 2

    # 사각형 한 바퀴를 도는 꼭짓점 번호 (0: 좌상단, 1: 우상단, 2: 우하단, 3: 좌하단)
    for corner in range(4):
        for step in range(RECT_STEPS + 1):
            if corner == 0:
                # 위쪽 변을 왼쪽에서 오른쪽으로 이동
                x = left + (right - left) * step / RECT_STEPS
                y = top
            elif corner == 1:
                # 오른쪽 변을 위에서 아래로 이동
                x = right
                y = top + (bottom - top) * step / RECT_STEPS
            elif corner == 2:
                # 아래쪽 변을 오른쪽에서 왼쪽으로 이동
                x = right - (right - left) * step / RECT_STEPS
                y = bottom
            else:
                # 왼쪽 변을 아래에서 위로 이동
                x = left
                y = bottom - (bottom - top) * step / RECT_STEPS

            # 캐릭터 이미지 표시
            draw_character(x, y)

def move_triangle():
    print("TRIANGLE")

    # 이동 순서대로 꼭짓점을 나열
    vertices = [TRI_TOP, TRI_RIGHT, TRI_LEFT]

    # 삼각형 한 바퀴를 도는 변 번호
    for edge in range(3):
        for step in range(TRI_STEPS + 1):
            # 이번 변의 시작점과 끝점
            x1, y1 = vertices[edge]
            x2, y2 = vertices[(edge + 1) % 3]
            t = step / TRI_STEPS

            # 시작점과 끝점 사이에서 x 좌표 보간
            x = x1 + (x2 - x1) * t

            # 시작점과 끝점 사이에서 y 좌표 보간
            y = y1 + (y2 - y1) * t

            # 캐릭터 이미지 표시
            draw_character(x, y)

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    delay(PAUSE)

close_canvas()

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

# 한 변을 몇 번에 나눠 이동할지 정하는 상수
STEPS_PER_SIDE = 20

# 삼각형 꼭짓점 좌표 (위쪽, 오른쪽 아래, 왼쪽 아래)
TRI_TOP = (CENTER_X, CENTER_Y - RADIUS)
TRI_RIGHT = (CENTER_X + RADIUS, CENTER_Y + RADIUS)
TRI_LEFT = (CENTER_X - RADIUS, CENTER_Y + RADIUS)

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

    # 지금 이동하고 있는 꼭짓점 번호 (0: 좌상단, 1: 우상단, 2: 우하단, 3: 좌하단)
    corner = 0

    while True:
        for step in range(STEPS_PER_SIDE + 1):
            if corner == 0:
                # 위쪽 변을 왼쪽에서 오른쪽으로 이동
                x = left + (right - left) * step / STEPS_PER_SIDE
                y = top
            elif corner == 1:
                # 오른쪽 변을 위에서 아래로 이동
                x = right
                y = top + (bottom - top) * step / STEPS_PER_SIDE
            elif corner == 2:
                # 아래쪽 변을 오른쪽에서 왼쪽으로 이동
                x = right - (right - left) * step / STEPS_PER_SIDE
                y = bottom
            else:
                # 왼쪽 변을 아래에서 위로 이동
                x = left
                y = bottom - (bottom - top) * step / STEPS_PER_SIDE

            # 캐릭터 이미지 표시
            clear_canvas()
            character.draw(x, y)
            update_canvas()
            delay(X_FRAME)

        # 한 변을 다 이동했으면 다음 꼭짓점으로
        corner += 1
        if corner == 4:
            corner = 0

def move_triangle():
    print("TRIANGLE")

    # 이동 순서대로 꼭짓점을 나열
    vertices = [TRI_TOP, TRI_RIGHT, TRI_LEFT]

    # 지금 이동하고 있는 변 번호
    edge = 0

    while True:
        for step in range(STEPS_PER_SIDE + 1):
            # 이번 변의 시작점과 끝점
            x1, y1 = vertices[edge]
            x2, y2 = vertices[(edge + 1) % 3]
            t = step / STEPS_PER_SIDE

            # 시작점과 끝점 사이에서 x 좌표 보간
            x = x1 + (x2 - x1) * t

            # 시작점과 끝점 사이에서 y 좌표 보간
            y = y1 + (y2 - y1) * t

            # 캐릭터 이미지 표시
            clear_canvas()
            character.draw(x, y)
            update_canvas()
            delay(X_FRAME)

        # 한 변을 다 이동했으면 다음 변으로
        edge += 1
        if edge == 3:
            edge = 0

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    delay(X_FRAME)

close_canvas()
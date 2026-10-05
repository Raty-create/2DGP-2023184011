from pico2d import *
from collections import namedtuple

# renderer는 open_canvas()를 호출한 뒤에 만들어지므로 star import로는
# 이 파일에서 바로 쓸 수 없다. 진행 표시줄처럼 SDL을 직접 그릴 때는
# 모듈을 p2d로 붙잡고 p2d.renderer를 넘긴다.
from pico2d import pico2d as p2d

# 한 프레임 = 스프라이트 시트 안의 사각형 영역.
# left는 시트 왼쪽에서 센 x좌표, width/height는 잘라낼 크기다.
# bottom은 시트 아래쪽 끝에서 위로 센 y좌표다. clip_draw가
# src_rect를 (left, 시트높이 - bottom - height)로 만들기 때문에 이 기준을 반드시 따라야 한다.
Frame = namedtuple("Frame", "left bottom width height")

# 뷰어가 그릴 캔버스의 크기. LEC08의 animation_viewer.py와 같은 해상도를 쓴다.
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

# 뷰어가 재생할 스프라이트 시트. 뷰어와 같은 폴더에 둔다.
SPRITE_SHEET_FILE = "sonic-sprite.png"

# 원본 프레임 최대 높이는 45px다. 45 * 4 = 180px로 확대하면 600px 높이 화면의
# 삼분의 1을 차지해 동작 자세가 선명하게 보인다. 더 크게 하면 잘려 나간다.
CHARACTER_SCALE = 4

# 한 프레임을 화면에 보여 주는 시간이다. 1 / 0.08 = 12.5fps.
# 프레임이 4개짜리 액션은 0.32초, 12개짜리 액션은 0.96초가 되어
# 어느 액션도 너무 빠르지도 느리지도 않은 박자에 들어간다.
FRAME_DURATION = 0.08

# FR-4.3. 특정 액션만 어색하면 여기에 그 액션 이름과 시간을 적는다.
# 공통값인 FRAME_DURATION은 그대로 두고, 적힌 액션에만 적용한다.
# 예) {"Death": 0.12} 라고 하면 Death만 8.3fps로 천천히 재생된다.
ACTION_FRAME_DURATION = {}

# 한 액션을 몇 번 반복한 뒤 다음 액션으로 넘어갈지 정한다.
REPEAT_COUNT = 5

# REPEAT_COUNT회 반복이 끝난 뒤 다음 액션으로 넘어가기 전에 멈춰 있는 시간이다.
PAUSE_TIME = 1.0

# 캐릭터가 서 있는 바닥선. 프레임마다 높이가 다르므로
# 프레임의 아래쪽 끝을 이 기준선에 맞춰 그린다.
# 최대 표시 높이 180px를 감안해 화면 중앙(300)보다 아래에 둔다.
GROUND_Y = 380

# 화면 위에 액션 이름과 진행 표시줄을 그릴 때 쓰는 글꼴이다.
# 액션 이름은 영문이라 어떤 시스템 폰트에서도 폭이 비슷해 굴림체를 쓴다.
UI_FONT_FILE = "C:/Windows/Fonts/malgun.ttf"
UI_FONT_SIZE = 20

# 액션 이름을 화면 어느 위치에 그릴지 정한다.
# 캐릭터는 화면 중앙에 있으므로 이름은 화면 왼쪽 위에 둔다.
# 글꼴의 draw는 글자의 중심을 받는다. y가 클수록 화면 위로 올라가므로
# 화면 맨 위(화면 기준 20px 부근)에 보이려면 600 - 20 - 높이/2 인 큰 값을 준다.
UI_TEXT_X = 20
UI_TEXT_Y = 570

# 반복 횟수 인디케이터를 그릴 영역이다. FR-6.1은 반복 횟수를 5칸으로
# 나타내기를 요구하므로 한 칸에 해당하는 폭과 칸 사이 간격을 상수로 둔다.
# 캐릭터 그림과 겹치지 않게 화면 아래에 배치한다.
UI_BAR_LEFT = 100
UI_BAR_TOP = CANVAS_HEIGHT - 40
UI_CELL_WIDTH = 80
UI_CELL_HEIGHT = 14
UI_CELL_GAP = 10
# 칸은 채웠을 때와 비웠을 때를 구분해 보여 준다.
UI_CELL_FILLED_COLOR = (40, 110, 220)
UI_CELL_EMPTY_COLOR = (90, 90, 100)

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

# 알파 채널이 있는 투명 배경 시트이므로 캔버스만 지우면 된다.
# LEC08이 알파 없는 RGB 시트 때문에 쓰던 배경색 덮어쓰기는 필요 없다.
sheet = load_image(SPRITE_SHEET_FILE)

# 액션 이름과 진행 표시줄을 그릴 글꼴. 뷰어와 함께 배포하지 않고
# Windows가 기본으로 제공하는 굴림체를 경로로 가리킨다.
ui_font = load_font(UI_FONT_FILE, UI_FONT_SIZE)

# 뷰어가 무엇을 재생하는지 시작하자마자 확인하게 해준다.
print("sprite sheet loaded: %d x %d" % (sheet.w, sheet.h))

# Idle: 시트에서 첫 번째 액션 행. 11프레임.
# sonic 시트는 균일 격자가 아니라 행마다 프레임 크기가 다른 밀집 배치라
# (열, 행) 계산으로는 프레임을 얻을 수 없다. 좌표를 직접 재야 한다.
# 이 행의 발밑은 시트 아래에서 447px 지점이다.
# 뒤 2프레임은 낮게 앉은 자세라 실제 그림이 더 짧고, 위쪽 여백도 포함해
# bottom을 447로 통일했다. 그래야 액션이 바뀔 때 발 위치가 흔들리지 않는다.
IDLE_FRAMES = [
    Frame(  1, 447, 29, 39), Frame( 31, 447, 26, 38), Frame( 58, 447, 28, 39),
    Frame( 86, 447, 30, 38), Frame(118, 447, 30, 38), Frame(150, 447, 30, 38),
    Frame(182, 447, 29, 38), Frame(211, 447, 29, 38), Frame(240, 447, 29, 38),
    Frame(270, 447, 24, 32), Frame(302, 447, 29, 26),
]

# Walk: 시트 두 번째 액션 행. 12프레임.
# 이 행은 시트 전체 폭(399px)을 끝까지 쓴다. 마지막 2프레임(x >= 334)은
# 다른 행에서 쓰지 않는 우측 영역에 있지만 Idle의 뒤 2프레임과 마찬가지로
# 이 액션의 연속 프레임으로 본다.
# 발밑이 프레임마다 407~410으로 3px 어긋나므로 407로 통일했다.
WALK_FRAMES = [
    Frame(  8, 407, 26, 38), Frame( 37, 407, 27, 38), Frame( 65, 407, 31, 38),
    Frame( 97, 407, 37, 38), Frame(135, 407, 32, 38), Frame(170, 407, 32, 39),
    Frame(206, 407, 26, 39), Frame(238, 407, 24, 38), Frame(263, 407, 30, 38),
    Frame(295, 407, 36, 38), Frame(334, 407, 32, 38), Frame(370, 407, 29, 39),
]

# Run: 시트 세 번째 액션 행. 6프레임.
# 달리기 자세라 4프레임째만 위로 뻗어 43px로 가장 높다.
RUN_FRAMES = [
    Frame(  1, 361, 33, 43), Frame( 39, 361, 35, 42), Frame( 89, 361, 35, 41),
    Frame(130, 361, 34, 43), Frame(181, 361, 34, 42), Frame(228, 361, 33, 42),
]

# Dash: 시트 네 번째 액션 행. 9프레임.
# 몸을 낮춘 자세라 28~33px로 납작하고, 시트 안에 떠 있는 1~4px짜리
# 알파 점들이 따로 잡힌다. 프레임은 본체 영역만 잡았다.
DASH_FRAMES = [
    Frame(  1, 325, 29, 31), Frame( 36, 325, 28, 33), Frame( 67, 325, 30, 31),
    Frame( 98, 325, 31, 30), Frame(131, 325, 29, 32), Frame(162, 325, 29, 32),
    Frame(193, 325, 30, 30), Frame(230, 325, 31, 30), Frame(268, 325, 30, 30),
]

# LookUp: 시트 다섯 번째 액션 행. 6프레임.
# 고개를 들어 올려다보는 자세라 시트 전체에서 높이가 가장 낮다(27px).
LOOK_UP_FRAMES = [
    Frame(  1, 292, 30, 27), Frame( 36, 292, 29, 27), Frame( 70, 292, 29, 27),
    Frame(105, 292, 29, 27), Frame(139, 292, 29, 27), Frame(174, 292, 29, 27),
]

# Crouch: 시트 여섯 번째 액션 행. 6프레임.
# 웅크린 자세라 35~36px로 낮고 폭이 일정하다.
CROUCH_FRAMES = [
    Frame(  1, 251, 29, 35), Frame( 36, 251, 30, 35), Frame( 74, 251, 31, 35),
    Frame(111, 251, 31, 36), Frame(149, 251, 30, 35), Frame(186, 251, 31, 36),
]

# Roll: 시트 일곱 번째 액션 행. 6프레임.
# 앞 2프레임은 폭이 29~30px, 뒤 4프레임은 38~39px로 넓다.
# 구르는 동안 몸이 길어지는 모양이 그대로 담겨 있는 행이다.
ROLL_FRAMES = [
    Frame(  1, 207, 29, 35), Frame( 36, 207, 30, 35), Frame( 72, 207, 39, 32),
    Frame(123, 207, 39, 33), Frame(172, 207, 39, 32), Frame(218, 207, 38, 33),
]

# Push: 시트 여덟 번째 액션 행. 8프레임.
# 시트에서 높이가 가장 큰 행(45px)이다. 뒤 2프레임은 실제로는 27~28px 높이에
# 아래쪽에 놓여 있어, 위쪽 빈 영역까지 포함한 30px로 잘라야 다른 프레임과
# 발의 높이가 맞는다.
PUSH_FRAMES = [
    Frame(  1, 154, 24, 45), Frame( 31, 154, 29, 44), Frame( 65, 154, 20, 44),
    Frame( 90, 154, 25, 44), Frame(119, 154, 25, 44), Frame(149, 154, 20, 44),
    Frame(184, 154, 40, 30), Frame(232, 154, 39, 30),
]

# Hurt: 시트 아홉 번째 액션 행. 8프레임.
# 아픈 표정을 지은 자세로, 뒤로 젖히며 36~40px 높이로 달라진다.
# 발밑이 108~111로 어긋나므로 108로 통일했다.
HURT_FRAMES = [
    Frame(  1, 108, 27, 39), Frame( 31, 108, 31, 38), Frame( 64, 108, 31, 38),
    Frame( 99, 108, 33, 40), Frame(136, 108, 32, 38), Frame(176, 108, 33, 38),
    Frame(217, 108, 33, 38), Frame(254, 108, 33, 39),
]

# Death: 시트 열 번째 액션 행. 4프레임.
# 프레임이 4개뿐인 가장 짧은 행이다. 12.5fps로 돌면 사이클이 0.32초라
# 성급하게 느껴질 수 있어, 실제 재생 화면을 보고 조정 대상으로 남겨 둔다.
# 마지막 2프레임의 발밑은 59로, 앞 2프레임보다 3px 높다. 넘어지는 동작이라
# 오히려 실제 높이를 유지하려고 56과 59를 그대로 쓴다.
DEATH_FRAMES = [
    Frame(  6,  56, 34, 43), Frame( 49,  56, 34, 43), Frame( 96,  59, 23, 42),
    Frame(125,  59, 23, 42),
]

# SPRITE = (action 이름, 그 action의 frame tuple)들의 나열.
# 이 순서가 화면에 재생되는 순서이며, 마지막 다음에는 첫 번째로 돌아간다.
# 여기를 고치면 액션 추가·삭제만으로 목록이 바뀌고 재생 로직은 손대지 않아도 된다.
SPRITE = [
    ("Idle", IDLE_FRAMES),
    ("Walk", WALK_FRAMES),
    ("Run", RUN_FRAMES),
    ("Dash", DASH_FRAMES),
    ("LookUp", LOOK_UP_FRAMES),
    ("Crouch", CROUCH_FRAMES),
    ("Roll", ROLL_FRAMES),
    ("Push", PUSH_FRAMES),
    ("Hurt", HURT_FRAMES),
    ("Death", DEATH_FRAMES),
]

for name, frames in SPRITE:
    print("%-12s : %2d frames" % (name, len(frames)))


def screen_center():
    return CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2


def draw_fill_rect(x, y, width, height, color):
    """주어진 영역을 색으로 채운다."""
    if width <= 0 or height <= 0:
        # SDL_RenderFillRect는 폭이 0이어도 왼쪽 끝 1픽셀을 칠한다.
        # 아무것도 그릴 차례에는 얼룩이 남지 않도록 건너뛴다.
        return
    p2d.SDL_SetRenderDrawColor(p2d.renderer, color[0], color[1], color[2], 255)
    p2d.SDL_RenderFillRect(p2d.renderer, p2d.SDL_Rect(x, y, width, height))


def draw_repeat_indicator(repeat, total):
    """반복 횟수를 칸 total개로 나타낸다.

    FR-6.2에 따라 이미 마친 repeat칸만 채우고 남은 칸은 비운다.
    정지 구간에는 repeat가 total과 같으므로 5칸이 모두 채워진다. (FR-6.3)
    """
    for index in range(total):
        # 칸 사이 간격만큼 띄워 가로로 나란히 놓는다.
        x = UI_BAR_LEFT + index * (UI_CELL_WIDTH + UI_CELL_GAP)
        color = UI_CELL_FILLED_COLOR if index < repeat else UI_CELL_EMPTY_COLOR
        draw_fill_rect(x, UI_BAR_TOP, UI_CELL_WIDTH, UI_CELL_HEIGHT, color)


def draw_frame(frame, x, y, scale=1.0):
    # 앞의 네 값은 스프라이트 시트 안의 프레임 영역, 뒤의 두 값은 캔버스 좌표이다.
    # 마지막 두 값은 화면에 표시할 크기이므로, 잘라내는 크기와 배율을 분리할 수 있다.
    sheet.clip_draw(frame.left, frame.bottom,
                    frame.width, frame.height,
                    x, y, frame.width * scale, frame.height * scale)

# 화면에 재생 중인 액션 하나를 나타내는 상태.
# 지금 어느 액션의 몇 번째 프레임을 보고 있는지만 들고 있고,
# 시간이 얼마나 흘렀는지는 main이 따지도록 넘겨준다.
# restart를 호출하면 그 액션의 첫 프레임부터 다시 시작한다.
class ActionState:
    def __init__(self, action, frames):
        self.action = action
        self.frames = frames
        self.frame = 0
        # 이 액션을 몇 번 반복했는지 센다. REPEAT_COUNT에 닿으면 액션이 끝난다.
        self.repeat = 0
        # 이 액션의 한 프레임 표시 시간이다. ACTION_FRAME_DURATION에
        # 이름이 있으면 그 값을, 없으면 공통값 FRAME_DURATION을 쓴다.
        self.frame_duration = ACTION_FRAME_DURATION.get(action, FRAME_DURATION)

    def restart(self):
        self.frame = 0

    def current(self):
        return self.frames[self.frame]

    def is_last(self):
        return self.frame == len(self.frames) - 1

    def advance(self):
        """다음 프레임으로 한 칸 이동한다. 마지막 프레임이면 되돌아가지 않는다."""
        if self.frame < len(self.frames) - 1:
            self.frame += 1
            return True
        return False

    def is_complete(self):
        """REPEAT_COUNT회 반복을 모두 끝내고 정지 구간에 들어갔는지 알려 준다."""
        return self.repeat >= REPEAT_COUNT


# 이 뷰어는 사용자의 입력으로 재생 위치를 바꾸지 않는다.
# 시간이 흐르는 대로 SPRITE 목록을 순환하며 보여주기만 한다.
# 목록을 한 바퀴 돈 뒤 처음으로 돌아가는 위치다.
player = ActionState(*SPRITE[0])
action_index = 0
# 현재 프레임이 화면에 표시된 시각이다. FRAME_DURATION이 지나면 다음 프레임으로 간다.
# get_time()은 초 단위로 지나간 시간을 돌려준다. 내부에서 SDL_GetTicks()를
# 1000으로 나누기 때문에 FRAME_DURATION, PAUSE_TIME과 단위가 같다.
# 여기서 1000을 또 곱하면 프레임 하나에 80초가 걸려 멈춘 것처럼 보인다.
frame_started = get_time()
# 마지막 프레임에 도착한 시각을 저장한다. 이 시각부터 PAUSE_TIME 동안 멈춘다.
paused_at = None

running = True

while running:
    clear_canvas()

    # 현재 프레임만 그린다. 어느 액션의 몇 프레임인지는 player가 기억한다.
    x, _ = screen_center()
    frame = player.current()
    # clip_draw의 두 번째 좌표는 그림의 중심이다. 프레임마다 높이가 다르므로
    # 화면 중앙에 두면 액션이 바뀔 때 캐릭터가 들락날락한다.
    # 대신 발이 닿는 바닥선을 GROUND_Y에 고정하려 한다.
    # 확대한 높이의 절반을 더하면 그림의 아래쪽 끝이 정확히 GROUND_Y에 온다.
    y = GROUND_Y + frame.height * CHARACTER_SCALE / 2
    draw_frame(frame, x, y, CHARACTER_SCALE)

    # 지금 보고 있는 액션 이름과, 그 액션을 몇 번 반복했는지 표시한다.
    ui_font.draw(UI_TEXT_X, UI_TEXT_Y, "Action: %s" % player.action)
    draw_repeat_indicator(player.repeat, REPEAT_COUNT)

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    now = get_time()

    if paused_at is not None:
        # 정지 시간이 끝났으면 다음 액션으로 넘어간다.
        if now - paused_at >= PAUSE_TIME:
            action_index = (action_index + 1) % len(SPRITE)
            player = ActionState(*SPRITE[action_index])
            paused_at = None
            # 새 액션의 첫 프레임도 정해진 시간만큼 보여야 한다.
            # 이 값을 갱신하지 않으면 1초짜리 정지 시간이 이미 지난 것으로
            # 계산되어 첫 프레임이 1ms 만에 지나가 버린다. (FR-3.6)
            frame_started = now
    else:
        # 정지 시간이 아니면 이 액션의 프레임 시간마다 한 프레임씩 넘어간다.
        # 특정 액션만 다르게 재생하려면 ACTION_FRAME_DURATION에 이름을 적는다.
        if now - frame_started >= player.frame_duration:
            frame_started = now
            if not player.advance():
                # advance가 False를 준 것은 마지막 프레임에 도착했다는 뜻이다.
                # REPEAT_COUNT회 모두 돌았다면 액션 사이에 멈춘다.
                player.repeat += 1
                if player.repeat >= REPEAT_COUNT:
                    paused_at = now
                else:
                    player.restart()

    update_canvas()

close_canvas()
from build123d import *
from ocp_vscode import *

set_port(3939)

length = 300.0
width = 50.0
height = 25.0

# 새로운 위치 (길이 방향 비율)
bow_x = -length * 0.45
mid_x = 0
stern_x = length * 0.35

# 단면 위치 (X축 방향, bow → mid → stern)
bow_x = -length * 0.45
mid_x = 0
stern_x = length * 0.35

def make_half_ellipse_sketch(w, h, x_pos):
    """
    YZ 평면(법선=X축)에 놓인 반타원형 단면 Face 반환
    w : 단면 폭  (Y 방향 전폭)
    h : 단면 높이(Z 방향 전고)
    x_pos : 단면이 놓일 X 좌표
    """
    r        = w / 2                     # 반지름 = 반폭
    z_scale  = h / r                     # Z축 스케일(반타원 비율)

    # ▼ YZ 평면을 명시적으로 지정: x_dir=Y축, normal=X축
    yz_plane = Plane(
        origin = (x_pos, 0, 0),          # X축 위치 조정
        x_dir  = (0, 1, 0),              # 평면의 local‑x  → 전역 Y
        y_dir  = (0, 0, 1),              # 평면의 local‑y  → 전역 Z
        z_dir  = (1, 0, 0),              # 평면의 local‑z  → 전역 X
        # normal = (1, 0, 0)               # 평면 법선      → 전역 X
    )

    with BuildSketch(yz_plane) as sk:
        with BuildLine():
            #   ↱--- 전역 Y 방향 ---↰
            #   (-r,0)───▶───(r,0)   ← 평면의 local‑x축
            CenterArc(center=(0, 0), radius=r, start_angle=180, arc_size=180)
            Line(( r, 0), (-r, 0))       # 윗면 직선으로 닫기
        make_face()

        # Z 방향(전역 Z = 평면의 local‑y축)만 스케일 → 반타원
        scaled = scale(sk.sketch, (1, 1, z_scale))

    return scaled # 단면 Face 반환

# 💡 각 단면 생성
bow = make_half_ellipse_sketch(width * 0.15, height * 0.4, bow_x)
mid = make_half_ellipse_sketch(width * 1.0, height * 1.0, mid_x)
stern = make_half_ellipse_sketch(width * 0.3, height * 0.5, stern_x)

# show_object(bow)
# show_object(mid)
# show_object(stern)

# 배 밑부분(hull) 만들기
# with BuildPart() as hull:
#     loft([bow, mid, stern], mode=Mode.ADD)

# show(hull.part)

# 배 전체 만들기(Hull Loft + Cabin)
with BuildPart() as ship:
    # ——— Hull
    # NOTE: loft()는 안쪽 껍질만 만들기 때문에 "면"이 없음
    loft([bow, mid, stern], mode=Mode.ADD)

    # ——— Cabin (선실)
    # 박스 크기: 길이 20%, 폭 40%, 높이 40%
    cabin_length = length * 0.20
    cabin_width  = width  * 0.40
    cabin_height = height * 0.40
    cabin = Box(
            cabin_length,
            cabin_width,
            cabin_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((mid_x, 0, height)))  # 중앙(mid_x, 0) 위, Z=height 에 배치

show(ship.part)
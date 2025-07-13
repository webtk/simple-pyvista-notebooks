# Create B-Rep with build123d
# - build123d 는 CAD 연산 기능을 담은 python 모듈

from build123d import *
# from jupyter_cadquery import show
from ocp_vscode import *

set_port(3939)

# [Parameters]
pcb_length = 70 * MM
pcb_width = 30 * MM
pcb_height = 3 * MM

# [Code]
with BuildPart() as pcb:
    with BuildSketch():
        Rectangle(pcb_length, pcb_width)

        for i in range(65 // 5):
            x = i * 5 - 30
            with Locations((x, -15), (x, -10), (x, 10), (x, 15)):
                Circle(1, mode=Mode.SUBTRACT)
        for i in range(30 // 5 - 1):
            y = i * 5 - 10
            with Locations((30, y), (35, y)):
                Circle(1, mode=Mode.SUBTRACT)
        with GridLocations(60, 20, 2, 2):
            Circle(2, mode=Mode.SUBTRACT)
    extrude(amount=pcb_height)

show(pcb)
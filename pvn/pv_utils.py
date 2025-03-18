import numpy as np
import pyvista as pv

def load_sample_mesh():
    mesh = pv.read('data/10_30.stl')
    return mesh
    
def create_simple_mesh():
    points = np.array([
        [0.5, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.5, 1.0, 0.0],
    ])

    # 2) faces 배열 정의
    #    첫 원소 '4'는 꼭짓점 개수, 그 뒤로 점 인덱스
    faces = np.hstack([[4, 0, 1, 2, 3]])
    # 3) PolyData 생성
    square = pv.PolyData(points, faces)
    mesh = square.extrude_rotate(
        angle=270,
        capping=True,
        resolution=30,
        rotation_axis=(1,0,0)
    )
    return mesh

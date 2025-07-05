#!/usr/bin/env python3
"""
인터랙티브 Mesh 뷰어

10_30.stl 파일의 mesh를 로드하고 조작 가능한 UI를 제공합니다.
PyVista와 ipywidgets를 사용하여 구현되었습니다.

사용법:
    python interactive_mesh_viewer.py
"""

import pyvista as pv
import numpy as np
import ipywidgets as widgets
from IPython.display import display, HTML
import sys
import os

def load_mesh_info(stl_filepath):
    """STL 파일을 로드하고 mesh 정보를 출력"""
    try:
        mesh = pv.read(stl_filepath)
        
        print("=== Mesh 정보 ===")
        print(f"셀 개수: {mesh.n_cells:,}")
        print(f"정점 개수: {mesh.n_points:,}")
        print(f"경계: {mesh.bounds}")
        print(f"Manifold: {mesh.is_manifold}")
        print(f"부피: {mesh.volume:.2f}")
        print(f"표면적: {mesh.area:.2f}")
        
        # 메시의 중심점 계산
        center = mesh.center
        print(f"중심점: ({center[0]:.3f}, {center[1]:.3f}, {center[2]:.3f})")
        
        return mesh
    except Exception as e:
        print(f"Mesh 로드 중 오류 발생: {e}")
        return None

def create_control_panel():
    """제어 패널 위젯들을 생성"""
    
    # 정보 표시를 위한 HTML 위젯
    info_display = widgets.HTML(
        value="<h3>Mesh 정보</h3><p>마우스를 mesh 위에 올려보세요!</p>",
        layout=widgets.Layout(width='100%', height='200px', border='1px solid gray', overflow='auto')
    )
    
    # 카메라 제어 위젯들
    view_buttons = widgets.HBox([
        widgets.Button(description="등각뷰", layout=widgets.Layout(width='80px')),
        widgets.Button(description="정면뷰", layout=widgets.Layout(width='80px')),
        widgets.Button(description="측면뷰", layout=widgets.Layout(width='80px')),
        widgets.Button(description="위뷰", layout=widgets.Layout(width='80px')),
        widgets.Button(description="리셋", layout=widgets.Layout(width='80px')),
    ])
    
    # Picking 모드 선택
    picking_mode = widgets.Dropdown(
        options=['정점', '셀', '비활성화'],
        value='정점',
        description='Picking 모드:',
        layout=widgets.Layout(width='100%')
    )
    
    # 메시 속성 제어
    mesh_properties = widgets.VBox([
        widgets.HTML(value="<h4>Mesh 속성</h4>"),
        widgets.Checkbox(value=True, description='모서리 표시'),
        widgets.FloatSlider(value=1.0, min=0.1, max=2.0, step=0.1, description='투명도:', continuous_update=False),
        widgets.FloatSlider(value=0.5, min=0.1, max=2.0, step=0.1, description='모서리 두께:', continuous_update=False),
    ], layout=widgets.Layout(width='100%', border='1px solid gray'))
    
    # 전체 컨트롤 패널
    control_panel = widgets.VBox([
        widgets.HTML(value="<h3>제어 패널</h3>"),
        widgets.HTML(value="<h4>카메라 뷰</h4>"),
        view_buttons,
        widgets.HTML(value="<h4>Picking 모드</h4>"),
        picking_mode,
        mesh_properties,
        info_display
    ], layout=widgets.Layout(width='100%', height='100%', border='2px solid blue'))
    
    return control_panel, info_display, view_buttons, mesh_properties, picking_mode

def create_plotter(mesh):
    """Plotter를 생성하고 mesh를 추가"""
    
    # PyVista 설정 - trame 백엔드 사용
    pv.global_theme.jupyter_backend = 'trame'
    
    # Plotter 생성
    plotter = pv.Plotter(notebook=True, window_size=[800, 600])
    
    # Mesh 추가
    actor = plotter.add_mesh(mesh, show_edges=True, edge_color='black', line_width=0.5)
    
    # 카메라 위치 설정
    plotter.camera_position = 'iso'
    plotter.show_axes()
    plotter.show_grid()
    
    return plotter, actor

def setup_event_handlers(plotter, actor, info_display, view_buttons, mesh_properties, picking_mode, mesh):
    """이벤트 핸들러들을 설정 (클릭 기반)"""
    
    # 정점 클릭 시 정보 표시
    def on_point_pick(point):
        # point: (x, y, z) 좌표
        # 가장 가까운 정점 인덱스 찾기
        dists = np.linalg.norm(mesh.points - point, axis=1)
        point_id = int(np.argmin(dists))
        pt = mesh.points[point_id]
        info = f"<h3>정점 선택 정보</h3>"
        info += f"<p><strong>정점 ID:</strong> {point_id}</p>"
        info += f"<p><strong>좌표:</strong> ({pt[0]:.3f}, {pt[1]:.3f}, {pt[2]:.3f})</p>"
        try:
            connected_cells = mesh.point_cells(point_id)
            info += f"<p><strong>연결된 셀 개수:</strong> {len(connected_cells)}</p>"
        except:
            info += f"<p><strong>연결된 셀 정보:</strong> 확인 불가</p>"
        info_display.value = info

    # 셀 클릭 시 정보 표시
    def on_cell_pick(mesh_, idx):
        info = f"<h3>셀 선택 정보</h3>"
        info += f"<p><strong>셀 ID:</strong> {idx}</p>"
        try:
            cell = mesh.get_cell(idx)
            cell_points = cell.points
            info += f"<p><strong>셀 정점들:</strong></p>"
            for i, pt in enumerate(cell_points):
                info += f"<p>  정점 {i}: ({pt[0]:.3f}, {pt[1]:.3f}, {pt[2]:.3f})</p>"
        except:
            info += f"<p><strong>셀 정보:</strong> 확인 불가</p>"
        info_display.value = info

    # Picking 모드 토글 함수
    def toggle_picking_mode(change):
        # 기존 picking 비활성화
        plotter.disable_picking()
        
        if change['new'] == '정점':
            plotter.enable_point_picking(callback=on_point_pick, show_message=True, use_picker=False)
        elif change['new'] == '셀':
            plotter.enable_cell_picking(callback=on_cell_pick, show_message=True)
        else:
            # picking 비활성화 상태 유지
            pass

    # 카메라/mesh 속성 제어 함수들은 기존과 동일하게 유지
    def set_isometric_view(b):
        plotter.camera_position = 'iso'
        plotter.reset_camera()
        plotter.render()
    def set_front_view(b):
        plotter.camera_position = 'xy'
        plotter.reset_camera()
        plotter.render()
    def set_side_view(b):
        plotter.camera_position = 'yz'
        plotter.reset_camera()
        plotter.render()
    def set_top_view(b):
        plotter.camera_position = 'xz'
        plotter.reset_camera()
        plotter.render()
    def reset_camera(b):
        plotter.reset_camera()
        plotter.render()
    def update_edge_visibility(change):
        actor.GetProperty().SetEdgeVisibility(change['new'])
        plotter.render()
    def update_opacity(change):
        actor.GetProperty().SetOpacity(change['new'])
        plotter.render()
    def update_edge_width(change):
        actor.GetProperty().SetLineWidth(change['new'])
        plotter.render()
    
    # 버튼 이벤트 연결
    view_buttons.children[0].on_click(set_isometric_view)
    view_buttons.children[1].on_click(set_front_view)
    view_buttons.children[2].on_click(set_side_view)
    view_buttons.children[3].on_click(set_top_view)
    view_buttons.children[4].on_click(reset_camera)
    
    # 속성 변경 이벤트 연결
    mesh_properties.children[1].observe(update_edge_visibility, names='value')
    mesh_properties.children[2].observe(update_opacity, names='value')
    mesh_properties.children[3].observe(update_edge_width, names='value')
    
    # 기본적으로 정점 picking 활성화
    plotter.enable_point_picking(callback=on_point_pick, show_message=True, use_picker=False)

    # Picking 모드 선택 이벤트 연결
    picking_mode.observe(toggle_picking_mode, names='value')

def create_integrated_viewer(mesh):
    """통합된 뷰어를 생성하고 반환"""
    
    # 제어 패널 생성
    control_panel, info_display, view_buttons, mesh_properties, picking_mode = create_control_panel()
    
    # Plotter 생성
    plotter, actor = create_plotter(mesh)
    
    # 이벤트 핸들러 설정
    setup_event_handlers(plotter, actor, info_display, view_buttons, mesh_properties, picking_mode, mesh)
    
    # plotter를 ipywidgets로 변환
    plotter_widget = plotter.show(return_viewer=True)
    
    # 수평 분할 레이아웃 생성
    # 왼쪽: 제어 패널, 오른쪽: plotter
    split_layout = widgets.HBox([
        widgets.VBox([control_panel], layout=widgets.Layout(width='400px', height='600px')),
        widgets.VBox([plotter_widget], layout=widgets.Layout(width='800px', height='600px'))
    ], layout=widgets.Layout(
        width='1200px', 
        height='600px',
        border='2px solid black',
        display='flex',
        align_items='stretch'
    ))
    
    return split_layout

def main():
    """메인 함수"""
    
    # STL 파일 경로
    stl_filepath = 'data/10_30.stl'
    
    # 파일 존재 확인
    if not os.path.exists(stl_filepath):
        print(f"오류: {stl_filepath} 파일을 찾을 수 없습니다.")
        print("현재 디렉토리:", os.getcwd())
        return
    
    # Mesh 로드
    mesh = load_mesh_info(stl_filepath)
    if mesh is None:
        return
    
    # 통합된 뷰어 생성
    integrated_viewer = create_integrated_viewer(mesh)
    
    # 통합된 레이아웃 표시
    display(integrated_viewer)

if __name__ == "__main__":
    main() 
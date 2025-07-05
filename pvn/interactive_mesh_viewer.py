#!/usr/bin/env python3
"""
인터랙티브 Mesh 뷰어

10_30.stl 파일의 mesh를 로드하고 조작 가능한 UI를 제공합니다.
PyVista와 ipywidgets를 사용하여 구현되었습니다.

사용법:
    python interactive_mesh_viewer.py
"""

import pyvista as pv
import ipywidgets as widgets
from IPython.display import display
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
    
    # 카메라 제어 위젯들
    view_buttons = widgets.HBox([
        widgets.Button(description="등각뷰", layout=widgets.Layout(width='80px')),
        widgets.Button(description="정면뷰", layout=widgets.Layout(width='80px')),
        widgets.Button(description="측면뷰", layout=widgets.Layout(width='80px')),
        widgets.Button(description="위뷰", layout=widgets.Layout(width='80px')),
        widgets.Button(description="리셋", layout=widgets.Layout(width='80px')),
    ])
    
    # 메시 속성 제어
    mesh_properties = widgets.VBox([
        widgets.HTML(value="<h4>Mesh 속성</h4>"),
        widgets.Checkbox(value=True, description='모서리 표시'),
        widgets.FloatSlider(value=1.0, min=0.1, max=2.0, step=0.1, description='투명도:', continuous_update=False),
        widgets.FloatSlider(value=0.5, min=0.1, max=2.0, step=0.1, description='모서리 두께:', continuous_update=False),
    ], layout=widgets.Layout(width='100%', border='1px solid gray'))
    
    # picking 정보 표시를 위한 HTML 위젯
    info_display = widgets.HTML(
        value="<p>마우스 오른쪽 버튼을 클릭하여 정보를 확인하세요</p>",
        layout=widgets.Layout(width='100%', height='200px', border='1px solid gray', overflow='auto')
    )

    # 전체 컨트롤 패널
    control_panel = widgets.VBox([
        widgets.HTML(value="<h3>제어 패널</h3>"),
        widgets.HTML(value="<h4>카메라 뷰</h4>"),
        view_buttons,
        mesh_properties,
        widgets.HTML(value="<h4>선택 정보</h4>"),
        info_display,
    ], layout=widgets.Layout(width='100%', height='100%', border='2px solid blue'))
    
    return control_panel, view_buttons, mesh_properties, info_display

def create_plotter(mesh):
    """Plotter를 생성하고 mesh를 추가"""
    
    # PyVista 설정 - trame 백엔드 사용
    pv.global_theme.jupyter_backend = 'trame'
    
    # Plotter 생성
    plotter = pv.Plotter(notebook=True, window_size=[800, 600])
    
    # Mesh 추가
    actor = plotter.add_mesh(mesh, show_edges=True, edge_color='black', line_width=0.5, pickable=True)
    
    # 카메라 위치 설정
    plotter.camera_position = 'iso'
    plotter.show_axes()
    plotter.show_grid()
    
    return plotter, actor

def setup_event_handlers(plotter, actor, view_buttons, mesh_properties, info_display, mesh):
    """이벤트 핸들러들을 설정 (클릭 기반)"""
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
    
    def on_point_pick(element):
        info_display.value = f"<p>선택: {element}</p>"

    # 기본적으로 정점 picking 활성화
    plotter.enable_element_picking(callback=on_point_pick,show_message=False)
    
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

def create_integrated_viewer(mesh):
    """통합된 뷰어를 생성하고 반환"""
    
    # 제어 패널 생성
    control_panel, view_buttons, mesh_properties, info_display = create_control_panel()
    
    # Plotter 생성
    plotter, actor = create_plotter(mesh)
    
    # 이벤트 핸들러 설정
    setup_event_handlers(plotter, actor, view_buttons, mesh_properties, info_display, mesh)
    
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
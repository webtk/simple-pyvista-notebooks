#!/usr/bin/env python3
"""
인터랙티브 Mesh 뷰어

10_30.stl 파일의 mesh를 로드하고 조작 가능한 UI를 제공합니다.
PyVista와 ipywidgets를 사용하여 구현되었습니다.

사용법:
    viewer = InteractiveMeshViewer('data/10_30.stl')
    viewer.show()
"""

import pyvista as pv
import ipywidgets as widgets
from IPython.display import display
import os


class InteractiveMeshViewer:
    """인터랙티브 Mesh 뷰어 클래스"""
    
    def __init__(self, stl_filepath):
        """
        InteractiveMeshViewer 초기화
        
        Args:
            stl_filepath (str): STL 파일 경로
        """
        self.stl_filepath = stl_filepath
        self.mesh = None
        self.plotter = None
        self.actor = None
        self.control_panel = None
        self.view_buttons = None
        self.mesh_properties = None
        self.info_display = None
        self.integrated_viewer = None
        
        # PyVista 설정 - trame 백엔드 사용
        pv.global_theme.jupyter_backend = 'trame'
        
        # Mesh 로드
        self._load_mesh()
    
    def _load_mesh(self):
        """STL 파일을 로드하고 mesh 정보를 출력"""
        try:
            if not os.path.exists(self.stl_filepath):
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.stl_filepath}")
            
            self.mesh = pv.read(self.stl_filepath)
            self._print_mesh_info()
            
        except Exception as e:
            print(f"Mesh 로드 중 오류 발생: {e}")
            self.mesh = None
    
    def _print_mesh_info(self):
        """Mesh 정보를 출력"""
        if self.mesh is None:
            return
            
        print("=== Mesh 정보 ===")
        print(f"셀 개수: {self.mesh.n_cells:,}")
        print(f"정점 개수: {self.mesh.n_points:,}")
        print(f"경계: {self.mesh.bounds}")
        print(f"Manifold: {self.mesh.is_manifold}")
        print(f"부피: {self.mesh.volume:.2f}")
        print(f"표면적: {self.mesh.area:.2f}")
        
        # 메시의 중심점 계산
        center = self.mesh.center
        print(f"중심점: ({center[0]:.3f}, {center[1]:.3f}, {center[2]:.3f})")
    
    def _create_control_panel(self):
        """제어 패널 위젯들을 생성"""
        
        # 카메라 제어 위젯들
        self.view_buttons = widgets.HBox([
            widgets.Button(description="등각뷰", layout=widgets.Layout(width='80px')),
            widgets.Button(description="정면뷰", layout=widgets.Layout(width='80px')),
            widgets.Button(description="측면뷰", layout=widgets.Layout(width='80px')),
            widgets.Button(description="위뷰", layout=widgets.Layout(width='80px')),
            widgets.Button(description="리셋", layout=widgets.Layout(width='80px')),
        ])
        
        # 메시 속성 제어
        self.mesh_properties = widgets.VBox([
            widgets.HTML(value="<h4>Mesh 속성</h4>"),
            widgets.Checkbox(value=True, description='모서리 표시'),
            widgets.FloatSlider(value=1.0, min=0.1, max=2.0, step=0.1, description='투명도:', continuous_update=False),
            widgets.FloatSlider(value=0.5, min=0.1, max=2.0, step=0.1, description='모서리 두께:', continuous_update=False),
        ], layout=widgets.Layout(width='100%', border='1px solid gray'))
        
        # picking 정보 표시를 위한 HTML 위젯
        self.info_display = widgets.HTML(
            value="<p>마우스 오른쪽 버튼을 클릭하여 정보를 확인하세요</p>",
            layout=widgets.Layout(width='100%', height='200px', border='1px solid gray', overflow='auto')
        )

        # 전체 컨트롤 패널
        self.control_panel = widgets.VBox([
            widgets.HTML(value="<h3>제어 패널</h3>"),
            widgets.HTML(value="<h4>카메라 뷰</h4>"),
            self.view_buttons,
            self.mesh_properties,
            widgets.HTML(value="<h4>선택 정보</h4>"),
            self.info_display,
        ], layout=widgets.Layout(width='100%', height='100%', border='2px solid blue'))
    
    def _create_plotter(self):
        """Plotter를 생성하고 mesh를 추가"""
        
        # Plotter 생성
        self.plotter = pv.Plotter(notebook=True, window_size=[800, 600])
        
        # Mesh 추가
        self.actor = self.plotter.add_mesh(self.mesh, show_edges=True, edge_color='black', line_width=0.5, pickable=True)
        
        # 카메라 위치 설정
        self.plotter.camera_position = 'iso'
        self.plotter.show_axes()
        self.plotter.show_grid()
    
    def _setup_event_handlers(self):
        """이벤트 핸들러들을 설정 (클릭 기반)"""
        
        # 카메라 뷰 제어 함수들
        def set_isometric_view(b):
            self.plotter.camera_position = 'iso'
            self.plotter.reset_camera()
            self.plotter.render()
        
        def set_front_view(b):
            self.plotter.camera_position = 'xy'
            self.plotter.reset_camera()
            self.plotter.render()
        
        def set_side_view(b):
            self.plotter.camera_position = 'yz'
            self.plotter.reset_camera()
            self.plotter.render()
        
        def set_top_view(b):
            self.plotter.camera_position = 'xz'
            self.plotter.reset_camera()
            self.plotter.render()
        
        def reset_camera(b):
            self.plotter.reset_camera()
            self.plotter.render()
        
        # Mesh 속성 제어 함수들
        def update_edge_visibility(change):
            self.actor.GetProperty().SetEdgeVisibility(change['new'])
            self.plotter.render()
        
        def update_opacity(change):
            self.actor.GetProperty().SetOpacity(change['new'])
            self.plotter.render()
        
        def update_edge_width(change):
            self.actor.GetProperty().SetLineWidth(change['new'])
            self.plotter.render()
        
        def on_point_pick(element):
            self.info_display.value = f"<p>선택: {element}</p>"

        # 기본적으로 정점 picking 활성화
        self.plotter.enable_element_picking(callback=on_point_pick, show_message=False)
        
        # 버튼 이벤트 연결
        self.view_buttons.children[0].on_click(set_isometric_view)
        self.view_buttons.children[1].on_click(set_front_view)
        self.view_buttons.children[2].on_click(set_side_view)
        self.view_buttons.children[3].on_click(set_top_view)
        self.view_buttons.children[4].on_click(reset_camera)
        
        # 속성 변경 이벤트 연결
        self.mesh_properties.children[1].observe(update_edge_visibility, names='value')
        self.mesh_properties.children[2].observe(update_opacity, names='value')
        self.mesh_properties.children[3].observe(update_edge_width, names='value')
    
    def _create_integrated_viewer(self):
        """통합된 뷰어를 생성하고 반환"""
        
        # 제어 패널 생성
        self._create_control_panel()
        
        # Plotter 생성
        self._create_plotter()
        
        # 이벤트 핸들러 설정
        self._setup_event_handlers()
        
        # plotter를 ipywidgets로 변환
        plotter_widget = self.plotter.show(return_viewer=True)
        
        # 수평 분할 레이아웃 생성
        # 왼쪽: 제어 패널, 오른쪽: plotter
        self.integrated_viewer = widgets.HBox([
            widgets.VBox([self.control_panel], layout=widgets.Layout(width='400px', height='600px')),
            widgets.VBox([plotter_widget], layout=widgets.Layout(width='800px', height='600px'))
        ], layout=widgets.Layout(
            width='1200px', 
            height='600px',
            border='2px solid black',
            display='flex',
            align_items='stretch'
        ))
    
    def show(self):
        """뷰어를 표시"""
        if self.mesh is None:
            print("Mesh가 로드되지 않았습니다.")
            return None
        
        self._create_integrated_viewer()
        # display(self.integrated_viewer)
        return self.integrated_viewer
    
    def get_mesh(self):
        """로드된 mesh를 반환"""
        return self.mesh
    
    def get_plotter(self):
        """plotter를 반환"""
        return self.plotter
    
    def update_info_display(self, info):
        """정보 표시 영역을 업데이트"""
        if self.info_display:
            self.info_display.value = f"<p>{info}</p>"
    
    def set_mesh_property(self, property_name, value):
        """Mesh 속성을 설정"""
        if self.actor is None:
            return
        
        if property_name == 'opacity':
            self.actor.GetProperty().SetOpacity(value)
        elif property_name == 'edge_visibility':
            self.actor.GetProperty().SetEdgeVisibility(value)
        elif property_name == 'edge_width':
            self.actor.GetProperty().SetLineWidth(value)
        
        if self.plotter:
            self.plotter.render() 

from typing import List
import pyvista as pv
import numpy as np
from ipywidgets import (
    VBox, HBox, Button, Label, Text, Checkbox, 
    Dropdown, HTML, Output, Layout
)
import ipywidgets as widgets
from IPython.display import display, clear_output

class MultiPlotterControlPanel:
    def __init__(self, plotters, actors, mesh_names):
        self.plotters = plotters
        self.actors = actors
        self.mesh_names = mesh_names
        self.picking_info = {}
        self.setup_ui()
        self.setup_picking_callbacks()
    
    def setup_ui(self):
        """UI 컴포넌트들을 설정합니다."""
        # Picking 정보 출력 영역
        self.picking_output = widgets.HTML(
            value="<p>마우스 오른쪽 버튼을 클릭하여 정보를 확인하세요</p>",
            layout=widgets.Layout(width='100%', height='200px', border='1px solid gray', overflow='auto')
        )
        
        # 카메라 동기화 관련 UI
        self.sync_camera_btn = Button(description="카메라 동기화", button_style='primary')
        self.sync_camera_btn.on_click(self.sync_cameras)
        
        # 기준 plotter 선택 체크박스들
        self.reference_checkboxes = []
        for i, name in enumerate(self.mesh_names):
            checkbox = Checkbox(description=f"{name} 기준", value=(i==0))
            self.reference_checkboxes.append(checkbox)
        
        # 개별 plotter 제어 버튼들
        self.reset_camera_btns = []
        self.reset_clipping_btns = []
        
        for i, name in enumerate(self.mesh_names):
            reset_cam_btn = Button(description=f"{name} 카메라 리셋", button_style='info')
            reset_cam_btn.on_click(lambda btn, idx=i: self.reset_camera(idx))
            self.reset_camera_btns.append(reset_cam_btn)
            
            reset_clip_btn = Button(description=f"{name} 클리핑 리셋", button_style='warning')
            reset_clip_btn.on_click(lambda btn, idx=i: self.reset_clipping(idx))
            self.reset_clipping_btns.append(reset_clip_btn)
        
        # 모든 plotter 제어 버튼들
        self.reset_all_camera_btn = Button(description="모든 카메라 리셋", button_style='success')
        self.reset_all_camera_btn.on_click(self.reset_all_cameras)
        
        self.reset_all_clipping_btn = Button(description="모든 클리핑 리셋", button_style='danger')
        self.reset_all_clipping_btn.on_click(self.reset_all_clipping)
        
        # UI 레이아웃 구성
        self.create_layout()
    
    def create_layout(self):
        """UI 레이아웃을 구성합니다."""
        # 카메라 동기화 섹션
        sync_header = HTML(value="<h4>카메라 동기화</h4>")
        reference_box = VBox([Label("기준 plotter 선택:")] + self.reference_checkboxes)
        sync_section = VBox([sync_header, reference_box, self.sync_camera_btn])
        
        # 개별 제어 섹션
        individual_header = HTML(value="<h4>개별 Plotter 제어</h4>")
        individual_controls = []
        for i in range(len(self.mesh_names)):
            control_row = HBox([self.reset_camera_btns[i], self.reset_clipping_btns[i]])
            individual_controls.append(control_row)
        
        individual_section = VBox([individual_header] + individual_controls)
        
        # 전체 제어 섹션
        global_header = HTML(value="<h4>전체 제어</h4>")
        global_controls = HBox([self.reset_all_camera_btn, self.reset_all_clipping_btn])
        global_section = VBox([global_header, global_controls])
        
        # Picking 정보 섹션
        picking_header = HTML(value="<h4>Picking 정보</h4>")
        picking_section = VBox([picking_header, self.picking_output])
        
        # 전체 레이아웃
        self.control_panel = VBox([
            sync_section,
            individual_section,
            global_section,
            picking_section
        ], layout=Layout(width='400px', border='2px solid gray', padding='10px'))
    
    def setup_picking_callbacks(self):
        """각 plotter에 picking 콜백을 설정합니다."""
        for _, plotter in enumerate(self.plotters):
            plotter.enable_element_picking(callback=self.on_pick, show_message=False)
    
    def on_pick(self, element):
        """Picking 이벤트를 처리합니다."""
        self.picking_output.value = f"<p>선택: {element}</p>"
    
    def get_reference_plotter_index(self):
        """기준이 되는 plotter의 인덱스를 반환합니다."""
        for i, checkbox in enumerate(self.reference_checkboxes):
            if checkbox.value:
                return i
        return 0  # 기본값
    
    def sync_cameras(self, button):
        """선택된 기준 plotter의 카메라를 다른 plotter들과 동기화합니다."""
        ref_idx = self.get_reference_plotter_index()
        ref_plotter = self.plotters[ref_idx]
        
        # 기준 plotter의 카메라 정보 가져오기
        camera = ref_plotter.camera
        
        # 다른 plotter들의 카메라를 동기화
        for i, plotter in enumerate(self.plotters):
            if i != ref_idx:
                plotter.camera = camera
                plotter.render()
        
        print(f"카메라가 {self.mesh_names[ref_idx]}를 기준으로 동기화되었습니다.")
    
    def reset_camera(self, plotter_index):
        """특정 plotter의 카메라를 리셋합니다."""
        self.plotters[plotter_index].reset_camera()
        print(f"{self.mesh_names[plotter_index]}의 카메라가 리셋되었습니다.")
    
    def reset_clipping(self, plotter_index):
        """특정 plotter의 클리핑을 리셋합니다."""
        self.plotters[plotter_index].disable_clipping()
        print(f"{self.mesh_names[plotter_index]}의 클리핑이 리셋되었습니다.")
    
    def reset_all_cameras(self, button):
        """모든 plotter의 카메라를 리셋합니다."""
        for plotter in self.plotters:
            plotter.reset_camera()
        print("모든 plotter의 카메라가 리셋되었습니다.")
    
    def reset_all_clipping(self, button):
        """모든 plotter의 클리핑을 리셋합니다."""
        for plotter in self.plotters:
            plotter.disable_clipping()
        print("모든 plotter의 클리핑이 리셋되었습니다.")
    
    def display(self):
        """Control panel을 화면에 표시합니다."""
        display(self.control_panel)

class MultiMeshViewer:
    meshes: List[pv.PolyData]
    plotters: List[pv.Plotter]
    actors: List[pv.Actor]
    control_panel: MultiPlotterControlPanel

    def __init__(self, meshes):
        self.meshes = meshes
        self.mesh_names = [f"mesh_{i}" for i, _ in enumerate(meshes)]
        self._create_plotters(self.meshes, self.mesh_names)
        self.control_panel = MultiPlotterControlPanel(self.plotters, self.actors, self.mesh_names)
    
    def _create_plotters(self, meshes, mesh_names):
        self.actors = []
        self.plotters = []
        for mesh, name in zip(meshes, mesh_names):
            plotter = pv.Plotter(title=name)
            actor = plotter.add_mesh(mesh, pickable=True)
            self.actors.append(actor)
            self.plotters.append(plotter)

    def show(self):
        plotter_widgets = [plotter.show(return_viewer=True) for plotter in self.plotters]
        integrated_viewer = widgets.HBox([self.control_panel.control_panel, *plotter_widgets])
        display(integrated_viewer)
        # return integrated_viewer
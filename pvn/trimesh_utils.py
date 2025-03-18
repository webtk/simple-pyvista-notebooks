import trimesh
import pyvista as pv

def pv_to_trimesh(pv_mesh:pv.PolyData) -> trimesh.Trimesh:
    """
    PyVista PolyData를 Trimesh 객체로 변환
    
    Parameters:
    -----------
    pv_mesh : pyvista.PolyData
        변환할 PyVista mesh
    
    Returns:
    --------
    trimesh.Trimesh
        변환된 Trimesh 객체
    """
    mesh = pv_mesh.triangulate()
    # vertices와 faces 추출
    vertices = mesh.points
    faces = mesh.faces.reshape(-1, 4)[:, 1:4]  # 첫 번째 열(셀 타입) 제외
    
    # Trimesh 객체 생성
    tri_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    return tri_mesh
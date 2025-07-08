from typing import List
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopLoc import TopLoc_Location
import pyvista as pv
import numpy as np


def load_brep(filepath):
    shape = TopoDS_Shape()
    builder = BRep_Builder()

    success = breptools_Read(shape, filepath, builder)
    if not success:
        raise RuntimeError(f"Failed to load BREP file: {filepath}")

    mesh = BRepMesh_IncrementalMesh(shape, 0.5)
    mesh.Perform()
    return shape

def show_face_count(shape):
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    count = 0
    while explorer.More():
        count += 1
        explorer.Next()
    print(f"Face count: {count}")


def extract_faces_to_pyvista(org_shape) -> List[pv.PolyData]:
    explorer = TopExp_Explorer(org_shape, TopAbs_FACE)
    faces_polydata = []

    while explorer.More():
        shape = explorer.Current()
        face = TopoDS_Face()
        face.TShape(shape.TShape())
        face.Location(shape.Location())
        face.Orientation(shape.Orientation())

        location = TopLoc_Location()
        triangulation = BRep_Tool.Triangulation(face, location)

        if triangulation:
            nb_nodes = triangulation.NbNodes()
            points = np.array([
                [triangulation.Node(i).X(), triangulation.Node(
                    i).Y(), triangulation.Node(i).Z()]
                for i in range(1, nb_nodes + 1)
            ])

            nb_tris = triangulation.NbTriangles()
            faces = []
            for i in range(1, nb_tris + 1):
                tri = triangulation.Triangle(i)
                idx = [tri.Value(j) - 1 for j in range(1, 4)]
                faces.append([3, *idx])

            # PyVista 형상 생성
            polydata = pv.PolyData(points, np.array(faces, dtype=np.int32))
            faces_polydata.append(polydata)

        explorer.Next()

    return faces_polydata

# 4. PyVista 시각화


def show_pyvista_meshes(polydata_list):
    plotter = pv.Plotter()
    for pd in polydata_list:
        plotter.add_mesh(pd, color="lightgray", show_edges=True)
    plotter.show()

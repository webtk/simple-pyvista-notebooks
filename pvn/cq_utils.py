import cadquery as cq
import numpy as np
import pyvista as pv
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.STEPControl import STEPControl_Reader
from OCP.BRep import BRep_Builder
from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakeFace,
                                BRepBuilderAPI_MakePolygon,
                                BRepBuilderAPI_MakeShell,
                                BRepBuilderAPI_MakeSolid,
                                BRepBuilderAPI_Sewing)
from OCP.gp import gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.StlAPI import StlAPI_Writer
from OCP.TopoDS import TopoDS_Compound


def load_step_file(path: str) -> cq.Shape:
    reader = STEPControl_Reader()
    status = reader.ReadFile(path)

    if status != IFSelect_RetDone:
        raise RuntimeError(f"Failed to read STEP file: {path}")

    reader.TransferRoots()

    # Get the number of shapes in the STEP file
    num_shapes = reader.NbShapes()
    if num_shapes == 0:
        raise RuntimeError(f"No shapes found in STEP file: {path}")

    # Iterate through the shapes and convert them to cq.Shape
    # If the STEP file contains multiple shapes, you might want to return a list of cq.Shape
    # For now, let's assume we are interested in the first shape or the only shape
    
    # Get the first shape
    occ_shape_raw = reader.Shape(1) # STEPControl_Reader.Shape() is 1-indexed

    # Check if the shape is a solid, and if so, cast it appropriately
    # This addresses the TypeError where a TopoDS_Solid was passed to downcast expecting TopoDS_Shape
    if occ_shape_raw.IsNull():
        raise RuntimeError(f"Failed to retrieve shape from STEP file: {path}")

    # CadQuery's cq.Shape constructor can often handle various TopoDS_Shape types directly.
    # The issue might be with downcast_LUT if it's strictly checking for TopoDS_Shape
    # but receiving a more specific type like TopoDS_Solid and then trying to re-cast it.
    # Let's try to directly use the obtained OCC shape.
    
    try:
        # STEP 파일이 대부분 단일 솔리드 형식을 가질 것이므로, cq.Solid로 바로 변환을 시도합니다.
        # 이 방법은 downcast_LUT의 특정 Solid_s() 호출 문제를 우회할 수 있습니다.
        return cq.Solid(occ_shape_raw)
    except Exception as e:
        # 만약 Solid가 아니라 다른 타입(예: Shell, Face 등)이라면 이 예외가 발생할 수 있습니다.
        # 이 경우에는 일반 cq.Shape로 다시 시도합니다.
        print(f"cq.Solid로 변환 시도 중 오류 발생: {e}. 일반 cq.Shape로 다시 시도합니다.")
        return cq.Shell(occ_shape_raw)

def triangle_face_from_indices(points, i0, i1, i2):
    """정점 인덱스로부터 OCC face 생성"""
    pts = [gp_Pnt(*points[i]) for i in (i0, i1, i2)]
    wire_builder = BRepBuilderAPI_MakePolygon()
    for pt in pts + [pts[0]]:  # 닫힌 루프
        wire_builder.Add(pt)
    wire_builder.Close()
    face = BRepBuilderAPI_MakeFace(wire_builder.Wire()).Face()
    return face

def pyvista_to_cadquery_solid_directly(pv_mesh: pv.PolyData) -> cq.Shape:
    faces = pv_mesh.faces.reshape(-1, 4)  # [3, i0, i1, i2]
    points = pv_mesh.points

    # Compound (Shell 역할)
    builder = BRep_Builder()
    comp = TopoDS_Compound()
    builder.MakeCompound(comp)

    for face in faces:
        if face[0] != 3:
            continue  # 삼각형만 처리
        i0, i1, i2 = face[1:]
        topo_face = triangle_face_from_indices(points, i0, i1, i2)
        builder.Add(comp, topo_face)

    # Compound → Solid
    solid_maker = BRepBuilderAPI_MakeSolid()
    solid_maker.Add(comp)
    if not solid_maker.IsDone():
        raise RuntimeError("Solid creation failed: probably the shell is not closed")

    solid = solid_maker.Solid()
    return cq.Shape(solid)

def triangle_face_from_pts(p0, p1, p2):
    """삼각형 face를 만드는 도우미 함수"""
    poly = BRepBuilderAPI_MakePolygon()
    for pt in [p0, p1, p2, p0]:  # close the loop
        poly.Add(pt)
    poly.Close()
    wire = poly.Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    return face

def pyvista_to_cadquery_solid(pv_mesh: pv.PolyData) -> cq.Shape:
    points = pv_mesh.points
    faces = pv_mesh.faces.reshape(-1, 4)  # [3, i0, i1, i2]

    sewing = BRepBuilderAPI_Sewing()
    for face in faces:
        if face[0] != 3:
            continue  # 삼각형만 처리
        i0, i1, i2 = face[1:]
        p0 = gp_Pnt(*points[i0])
        p1 = gp_Pnt(*points[i1])
        p2 = gp_Pnt(*points[i2])
        face_obj = triangle_face_from_pts(p0, p1, p2)
        sewing.Add(face_obj)

    sewing.Perform()
    shell = sewing.SewedShape()

    # shell → solid
    solid_maker = BRepBuilderAPI_MakeSolid()
    solid_maker.Add(cq.Shape(shell).wrapped)
    solid = solid_maker.Solid()

    return cq.Shape(solid)

def export_cq_shape_to_step(shape: cq.Shape, filename: str):
    """CadQuery Shape → STEP 파일 저장"""
    writer = STEPControl_Writer()
    writer.Transfer(shape.wrapped, STEPControl_AsIs)
    status = writer.Write(filename)
    if status != IFSelect_RetDone:
        raise RuntimeError("Failed to export STEP file")
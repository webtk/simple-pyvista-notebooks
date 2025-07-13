import pyvista as pv
#from jupyter_cadquery import show
from ocp_vscode import *

from pvn.cq_utils import export_cq_shape_to_step, pyvista_to_cadquery_solid

set_port(3939)

mesh = pv.read('../../data/10_30.stl')
decimated_mesh = mesh.decimate_pro(0.9)

# 이 작업은 mesh의 cell이 많은 경우 오래 걸림
cq_solid = pyvista_to_cadquery_solid(mesh)

# Solid를 파일로 저장(STEP)
# 파일이 매우 클 수 있음(수십MB)
export_cq_shape_to_step(cq_solid, "../../data/10_30.step")
show(cq_solid)
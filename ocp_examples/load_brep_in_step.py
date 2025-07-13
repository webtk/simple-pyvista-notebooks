# STEP 파일에서 B-rep 데이터 로드 및 메시 변환
# 1. OCC Core 사용해서 STEP 파일 로드
# 2. B-rep 데이터를 메시로 변환
# 3. PyVista를 사용하여 3D 시각화

from cadquery import importers

step_filepath = '../../data/fixed.step'
step_model = importers.importStep(step_filepath)
step_model
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/webtk/simple-pyvista-notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F00_introduction.ipynb)

# Simple Collection of Jupyter Notebooks for CAD, CAE application developers
 - A software engineer collected and conducted these codes in order to accelerate developing process for his own benefit.

## Quick Links
 - [Step 1. Make simple PolyData object and plot with basic plotter](notebooks/01.Plotting/01_load_and_plot.ipynb)
 - [Step 2. Practice basic operation on objects](notebooks/02.Basic_Mesh_Ops/)
 - [Step 3. Learn about implicit representation of object](notebooks/03.SDF/)

## Key Takeaways
### 1. Plotting meshes
 - Loading a mesh and visualize it in [Trame](https://kitware.github.io/trame/) client viewer for better interaction
 - Decimating meshes for faster rendering
### 2. Practicing basic operations on meshes
 - Extracting parts from a mesh
 - Revolving meshes
 - Reflecting meshes
 - Calculating curvature 
### 3. Implicit representation of objects
 - Converting a mesh to [Signed Distance Function](https://en.wikipedia.org/wiki/Signed_distance_function)(SDF) grid
 - Converting a SDF into mesh by marching cube

## TODO
 - Load field data and render it
 - Visualize load condition

 # Data Sources
  - [GRAB CAD Community Library](https://grabcad.com/library)
  - [Thingiverse](https://www.thingiverse.com/)
from setuptools import setup, find_packages

setup(
    name="pvn",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyvista",
        "numpy", 
        "pandas",
        "h5py",
        "trimesh",
        "ipywidgets",
        "vtk",
        "trame",
        "trame-vtk",
        "trame-client", 
        "trame-server",
        "trame-vuetify",
        "trame-jupyter-extension"
    ],
    python_requires=">=3.8",
) 
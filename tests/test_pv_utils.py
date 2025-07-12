import unittest
from unittest.mock import MagicMock, patch

import numpy as np
import pyvista as pv

from pvn.pv_utils import create_simple_mesh


def load_sample_mesh() -> pv.PolyData:
    return pv.Sphere()

class TestPVUtils(unittest.TestCase):
    @patch('pyvista.read')
    def test_load_sample_mesh(self, mock_read):
        # Mock the mesh object
        mock_mesh = MagicMock()
        mock_read.return_value = mock_mesh
        
        # Call the function
        result = load_sample_mesh()
        
        # Verify that pv.read was called with correct path
        mock_read.assert_called_once_with('data/10_30.stl')
        
        # Verify that the function returns the mesh
        self.assertEqual(result, mock_mesh)
    
    def test_create_simple_mesh(self):
        # Call the function
        mesh = create_simple_mesh()
        
        # Verify that the result is a PyVista mesh
        self.assertIsInstance(mesh, pv.PolyData)
        
        # Verify the mesh properties
        points = mesh.points
        self.assertEqual(points.shape[1], 3)  # Check if points are 3D (x,y,z)
        self.assertTrue(mesh.n_points > 0)  # Check if it has points
        self.assertTrue(mesh.n_faces > 0)  # Check if it has faces
        
        # Verify the mesh bounds
        bounds = mesh.bounds
        self.assertGreater(bounds[1], bounds[0])  # x bounds
        self.assertGreater(bounds[3], bounds[2])  # y bounds
        self.assertGreater(bounds[5], bounds[4])  # z bounds
        
        # Verify the mesh is not empty
        self.assertGreater(mesh.volume, 0)  # Check if it has volume

if __name__ == '__main__':
    unittest.main() 
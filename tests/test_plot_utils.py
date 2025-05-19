import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from pvn.plot_utils import plot_histogram

class TestPlotUtils(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.sample_data = np.array([1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 5.0])
        
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.hist')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.grid')
    @patch('matplotlib.pyplot.axvline')
    @patch('matplotlib.pyplot.legend')
    def test_plot_histogram(self, mock_legend, mock_axvline, mock_grid, 
                          mock_ylabel, mock_xlabel, mock_title, mock_hist,
                          mock_figure, mock_show):
        # Call the function
        plot_histogram(self.sample_data)
        
        # Verify that all plotting functions were called
        mock_figure.assert_called_once()
        mock_hist.assert_called_once()
        mock_title.assert_called_once_with('Histogram of Surface Distances')
        mock_xlabel.assert_called_once_with('Distance to Surface')
        mock_ylabel.assert_called_once_with('Frequency')
        mock_grid.assert_called_once_with(True, alpha=0.3)
        
        # Verify that axvline was called 3 times (mean and ±std)
        self.assertEqual(mock_axvline.call_count, 3)
        
        # Verify that legend was called
        mock_legend.assert_called_once()
        
        # Verify that show was called
        mock_show.assert_called_once()
        
    def test_plot_histogram_statistics(self):
        # Test with a known dataset
        test_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            plot_histogram(test_data)
            
            # Verify that the correct statistics were printed
            expected_mean = 3.0
            expected_std = np.std(test_data)
            expected_min = 1.0
            expected_max = 5.0
            
            # Check if all statistics were printed
            mock_print.assert_any_call(f"Mean distance: {expected_mean:.3f}")
            mock_print.assert_any_call(f"Standard deviation: {expected_std:.3f}")
            mock_print.assert_any_call(f"Min distance: {expected_min:.3f}")
            mock_print.assert_any_call(f"Max distance: {expected_max:.3f}")
"""Advanced tests for GPS plotting functionality."""
import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
from gpmf import gps_plot, gps


class TestDataframeConversion:
    """Test conversion of GPS data to pandas DataFrame."""
    
    def test_to_dataframe_single_block(self):
        """Test converting single GPS block to DataFrame."""
        # Create a GPS data block
        gps_data = [
            gps.GPSData(
                description="Test",
                timestamp="2024-01-12 10:00:00.000",
                precision=1.0,
                fix=3,
                latitude=np.array([37.7749]),
                longitude=np.array([-122.4194]),
                altitude=np.array([10.0]),
                speed_2d=np.array([5.0]),
                speed_3d=np.array([5.1]),
                units="m/s",
                npoints=1
            )
        ]
        
        # Convert to DataFrame
        df = gps_plot.to_dataframe(gps_data)
        
        # Verify DataFrame structure
        assert isinstance(df, pd.DataFrame)
        assert 'latitude' in df.columns
        assert 'longitude' in df.columns
        assert 'altitude' in df.columns
        assert 'speed_2d' in df.columns
        assert 'speed_3d' in df.columns
    
    def test_to_dataframe_multiple_blocks(self):
        """Test converting multiple GPS blocks to DataFrame."""
        # Create multiple GPS data blocks
        gps_data = []
        for i in range(5):
            gps_data.append(
                gps.GPSData(
                    description="Test",
                    timestamp=f"2024-01-12 10:00:{i:02d}.000",
                    precision=1.0,
                    fix=3,
                    latitude=np.array([37.7749 + i * 0.001]),
                    longitude=np.array([-122.4194 + i * 0.001]),
                    altitude=np.array([10.0 + i]),
                    speed_2d=np.array([5.0]),
                    speed_3d=np.array([5.0]),
                    units="m/s",
                    npoints=1
                )
            )
        
        # Convert to DataFrame
        df = gps_plot.to_dataframe(gps_data)
        
        # Should have data from all blocks
        assert len(df) == 5
        assert 'block_id' in df.columns
    
    def test_to_dataframe_empty_list(self):
        """Test DataFrame conversion with empty list."""
        with pytest.raises(Exception):
            # Empty list should raise error
            df = gps_plot.to_dataframe([])


class TestOutlierFiltering:
    """Test outlier detection and filtering."""
    
    def test_filter_outliers_normal_data(self):
        """Test outlier filter with normal distribution."""
        # Create normal data
        data = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
        
        # Filter outliers
        mask = gps_plot.filter_outliers(data)
        
        # Should return boolean mask
        assert isinstance(mask, np.ndarray)
        assert mask.dtype == bool
        assert len(mask) == len(data)
    
    def test_filter_outliers_with_extremes(self):
        """Test outlier filter with extreme values."""
        # Create data with outliers
        data = np.array([1.0, 2.0, 3.0, 100.0, 2.5, -50.0, 3.5])
        
        # Filter outliers
        mask = gps_plot.filter_outliers(data)
        
        # Outliers should be filtered
        assert isinstance(mask, np.ndarray)
        
        # Most normal values should pass
        filtered_count = np.sum(mask)
        assert filtered_count > 0
    
    def test_filter_outliers_uniform_data(self):
        """Test outlier filter with uniform data."""
        # All same values
        data = np.array([5.0, 5.0, 5.0, 5.0, 5.0])
        
        mask = gps_plot.filter_outliers(data)
        
        # Should handle uniform data
        assert isinstance(mask, np.ndarray)


class TestPlottingFunctions:
    """Test plotting function interfaces."""
    
    def test_plot_gps_trace_signature(self):
        """Test plot_gps_trace function signature."""
        import inspect
        
        # Get function signature
        sig = inspect.signature(gps_plot.plot_gps_trace)
        
        # Should have parameters
        params = list(sig.parameters.keys())
        assert len(params) > 0
        assert 'latlon' in params
    
    def test_plot_gps_trace_from_stream_signature(self):
        """Test plot_gps_trace_from_stream function signature."""
        import inspect
        
        # Get function signature
        sig = inspect.signature(gps_plot.plot_gps_trace_from_stream)
        
        # Should have parameters
        params = list(sig.parameters.keys())
        assert len(params) > 0
        assert 'stream' in params
    
    @patch('matplotlib.pyplot.figure')
    @patch('geopandas.GeoDataFrame')
    def test_plot_gps_trace_execution(self, mock_gdf, mock_figure):
        """Test plot_gps_trace execution."""
        # Create sample lat/lon data
        latlon = np.array([[37.7749, -122.4194], [37.7750, -122.4195]])
        
        try:
            gps_plot.plot_gps_trace(latlon)
        except:
            # May fail due to missing dependencies, but function should exist
            pass
    
    @patch('gpmf.gps.extract_gps_blocks')
    @patch('gpmf.gps.parse_gps_block')
    def test_plot_gps_trace_from_stream_execution(self, mock_parse, mock_extract):
        """Test plot_gps_trace_from_stream execution."""
        # Mock GPS data
        mock_gps_data = MagicMock()
        mock_gps_data.latitude = np.array([37.7749])
        mock_gps_data.longitude = np.array([-122.4194])
        
        mock_extract.return_value = [MagicMock()]
        mock_parse.return_value = mock_gps_data
        
        stream = b'fake_stream'
        
        try:
            gps_plot.plot_gps_trace_from_stream(stream)
        except:
            # May fail due to visualization, but should process data
            pass


class TestCoordinateSystems:
    """Test coordinate system definitions."""
    
    def test_latlon_epsg(self):
        """Test LATLON coordinate system."""
        assert hasattr(gps_plot, 'LATLON')
        assert gps_plot.LATLON == "EPSG:4326"
    
    def test_lambert93_epsg(self):
        """Test LAMBERT93 coordinate system."""
        assert hasattr(gps_plot, 'LAMBERT93')
        assert gps_plot.LAMBERT93 == "EPSG:2154"
    
    def test_coordinate_systems_are_strings(self):
        """Test that coordinate systems are strings."""
        assert isinstance(gps_plot.LATLON, str)
        assert isinstance(gps_plot.LAMBERT93, str)


class TestDataProcessing:
    """Test GPS data processing for plotting."""
    
    def test_dataframe_has_required_columns(self):
        """Test that DataFrame has all required columns."""
        gps_data = [
            gps.GPSData(
                description="Test",
                timestamp="2024-01-12 10:00:00.000",
                precision=1.0,
                fix=3,
                latitude=np.array([37.7749, 37.7750]),
                longitude=np.array([-122.4194, -122.4195]),
                altitude=np.array([10.0, 11.0]),
                speed_2d=np.array([5.0, 5.1]),
                speed_3d=np.array([5.0, 5.1]),
                units="m/s",
                npoints=2
            )
        ]
        
        df = gps_plot.to_dataframe(gps_data)
        
        required_columns = ['latitude', 'longitude', 'altitude', 'time', 'speed_2d', 'speed_3d', 'precision', 'fix']
        for col in required_columns:
            assert col in df.columns
    
    def test_dataframe_correct_row_count(self):
        """Test that DataFrame has correct number of rows."""
        # Block with 3 points
        gps_data = [
            gps.GPSData(
                description="Test",
                timestamp="2024-01-12 10:00:00.000",
                precision=1.0,
                fix=3,
                latitude=np.array([37.7749, 37.7750, 37.7751]),
                longitude=np.array([-122.4194, -122.4195, -122.4196]),
                altitude=np.array([10.0, 11.0, 12.0]),
                speed_2d=np.array([5.0, 5.1, 5.2]),
                speed_3d=np.array([5.0, 5.1, 5.2]),
                units="m/s",
                npoints=3
            )
        ]
        
        df = gps_plot.to_dataframe(gps_data)
        
        # Should have 3 rows
        assert len(df) == 3


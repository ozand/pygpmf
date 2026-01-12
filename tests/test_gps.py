"""Tests for GPS parsing functionality."""
import pytest
from gpmf import gps


class TestGPSParsing:
    """Test GPS data extraction and parsing."""
    
    def test_parse_gps_block_basic(self, sample_gps_data):
        """Test basic GPS block parsing."""
        # TODO: Implement with real GPMF data
        assert sample_gps_data['lat'] == pytest.approx(44.1287283, rel=1e-6)
        assert sample_gps_data['lon'] == pytest.approx(5.427715, rel=1e-6)
    
    def test_gps_altitude_parsing(self, sample_gps_data):
        """Test altitude extraction from GPS data."""
        assert sample_gps_data['alt'] == pytest.approx(833.759, rel=1e-3)
    
    def test_gps_speed_2d(self, sample_gps_data):
        """Test 2D speed calculation."""
        assert sample_gps_data['speed_2d'] > 0
        assert sample_gps_data['speed_2d'] == pytest.approx(9.221, rel=1e-3)
    
    def test_gps_speed_3d(self, sample_gps_data):
        """Test 3D speed calculation."""
        assert sample_gps_data['speed_3d'] >= sample_gps_data['speed_2d']
    
    def test_extract_gps_blocks(self, sample_gpmf_stream):
        """Test GPS block extraction from GPMF stream."""
        # TODO: Implement with real GPMF stream
        pytest.skip("Requires real GPMF test data")
    
    def test_make_gpx_segment(self):
        """Test GPX segment creation from GPS data."""
        # TODO: Implement GPX generation test
        pytest.skip("Requires GPS data list")


class TestGPSValidation:
    """Test GPS data validation."""
    
    def test_invalid_latitude(self):
        """Test handling of invalid latitude values."""
        # Latitude must be between -90 and 90
        # TODO: Implement validation
        pass
    
    def test_invalid_longitude(self):
        """Test handling of invalid longitude values."""
        # Longitude must be between -180 and 180
        # TODO: Implement validation
        pass
    
    def test_missing_gps_fix(self):
        """Test handling of missing GPS fix."""
        # TODO: Implement GPS fix status check
        pass

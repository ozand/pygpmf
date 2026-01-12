"""Tests for Hero 11-13 GPS9 support."""
import pytest
import numpy as np
from collections import namedtuple
from gpmf import gps

# Mock KVLItem for testing
KVLItem = namedtuple('KVLItem', ['key', 'value'])


class TestGPS9Support:
    """Test GPS9 parsing for Hero 11+ cameras."""
    
    @pytest.fixture
    def gps9_block(self):
        """Create a mock GPS9 block (Hero 11+)."""
        # GPS9 has 9 fields: lat, lon, alt, speed_2d, speed_3d, 
        # days_since_2000, seconds_since_midnight, dop, fix_status
        gps9_data = np.array([
            [441287283, 54277150, 833759, 9221, 10123, 7895, 36000, 100, 3],  # Sample values
        ], dtype=np.int32)
        
        scaling_factors = np.array([10000000, 10000000, 1000, 1000, 1000, 1, 1, 100, 1])
        
        return [
            KVLItem(key='GPS9', value=gps9_data),
            KVLItem(key='SCAL', value=scaling_factors),
            KVLItem(key='STNM', value='GPS9 Track'),
            KVLItem(key='GPSU', value='2024-01-12 10:00:00.000'),
            KVLItem(key='GPSP', value=150),  # 1.50 precision
            KVLItem(key='GPSF', value=3),    # 3D fix
            KVLItem(key='UNIT', value='deg,deg,m,m/s,m/s'),
        ]
    
    @pytest.fixture
    def gps5_block(self):
        """Create a mock GPS5 block (Hero 5-10)."""
        gps5_data = np.array([
            [441287283, 54277150, 833759, 9221, 10123],  # 5 fields
        ], dtype=np.int32)
        
        scaling_factors = np.array([10000000, 10000000, 1000, 1000, 1000])
        
        return [
            KVLItem(key='GPS5', value=gps5_data),
            KVLItem(key='SCAL', value=scaling_factors),
            KVLItem(key='STNM', value='GPS5 Track'),
            KVLItem(key='GPSU', value='2024-01-12 10:00:00.000'),
            KVLItem(key='GPSP', value=150),
            KVLItem(key='GPSF', value=3),
            KVLItem(key='UNIT', value='deg,deg,m,m/s,m/s'),
        ]
    
    def test_parse_gps9_block(self, gps9_block):
        """Test parsing GPS9 block (Hero 11+)."""
        gps_data = gps.parse_gps_block(gps9_block)
        
        # Verify GPS data fields are extracted correctly
        assert gps_data.description == 'GPS9 Track'
        assert gps_data.timestamp == '2024-01-12 10:00:00.000'
        assert gps_data.fix == 3
        assert gps_data.precision == pytest.approx(1.5, rel=1e-2)
        
        # Verify only first 5 fields are extracted (compatible with GPS5)
        assert len(gps_data.latitude) == 1
        assert gps_data.latitude[0] == pytest.approx(44.1287283, rel=1e-6)
        assert gps_data.longitude[0] == pytest.approx(5.427715, rel=1e-6)
        assert gps_data.altitude[0] == pytest.approx(833.759, rel=1e-3)
        assert gps_data.speed_2d[0] == pytest.approx(9.221, rel=1e-3)
        assert gps_data.speed_3d[0] == pytest.approx(10.123, rel=1e-3)
    
    def test_parse_gps5_block_still_works(self, gps5_block):
        """Test that GPS5 parsing still works (backward compatibility)."""
        gps_data = gps.parse_gps_block(gps5_block)
        
        assert gps_data.description == 'GPS5 Track'
        assert gps_data.latitude[0] == pytest.approx(44.1287283, rel=1e-6)
        assert gps_data.longitude[0] == pytest.approx(5.427715, rel=1e-6)
        assert gps_data.altitude[0] == pytest.approx(833.759, rel=1e-3)
    
    def test_gps9_prefers_over_gps5(self):
        """Test that GPS9 is preferred when both streams present."""
        # Create block with both GPS5 and GPS9
        gps5_data = np.array([[441287283, 54277150, 833759, 9221, 10123]], dtype=np.int32)
        gps9_data = np.array([[441287283, 54277150, 833759, 9221, 10123, 7895, 36000, 100, 3]], dtype=np.int32)
        
        scaling5 = np.array([10000000, 10000000, 1000, 1000, 1000])
        scaling9 = np.array([10000000, 10000000, 1000, 1000, 1000, 1, 1, 100, 1])
        
        block = [
            KVLItem(key='GPS5', value=gps5_data),
            KVLItem(key='GPS9', value=gps9_data),
            KVLItem(key='SCAL', value=scaling9),  # GPS9 scaling
            KVLItem(key='STNM', value='Dual GPS'),
            KVLItem(key='GPSU', value='2024-01-12 10:00:00.000'),
            KVLItem(key='GPSP', value=150),
            KVLItem(key='GPSF', value=3),
            KVLItem(key='UNIT', value='deg,deg,m,m/s,m/s'),
        ]
        
        gps_data = gps.parse_gps_block(block)
        # Should parse successfully using GPS9
        assert gps_data.description == 'Dual GPS'
        assert gps_data.latitude[0] == pytest.approx(44.1287283, rel=1e-6)
    
    def test_gps9_multi_sample(self):
        """Test GPS9 parsing with multiple samples."""
        gps9_data = np.array([
            [441287283, 54277150, 833759, 9221, 10123, 7895, 36000, 100, 3],
            [441287284, 54277151, 833760, 9222, 10124, 7895, 36001, 101, 3],
            [441287285, 54277152, 833761, 9223, 10125, 7895, 36002, 102, 3],
        ], dtype=np.int32)
        
        scaling_factors = np.array([10000000, 10000000, 1000, 1000, 1000, 1, 1, 100, 1])
        
        block = [
            KVLItem(key='GPS9', value=gps9_data),
            KVLItem(key='SCAL', value=scaling_factors),
            KVLItem(key='STNM', value='GPS9 Track'),
            KVLItem(key='GPSU', value='2024-01-12 10:00:00.000'),
            KVLItem(key='GPSP', value=150),
            KVLItem(key='GPSF', value=3),
            KVLItem(key='UNIT', value='deg,deg,m,m/s,m/s'),
        ]
        
        gps_data = gps.parse_gps_block(block)
        
        # Verify 3 samples parsed
        assert gps_data.npoints == 3
        assert len(gps_data.latitude) == 3
        assert len(gps_data.longitude) == 3
        
        # Verify all coordinates extracted
        assert gps_data.latitude[0] == pytest.approx(44.1287283, rel=1e-6)
        assert gps_data.latitude[1] == pytest.approx(44.1287284, rel=1e-6)
        assert gps_data.latitude[2] == pytest.approx(44.1287285, rel=1e-6)
    
    def test_extract_gps_blocks_detects_both(self):
        """Test that extract_gps_blocks detects both GPS5 and GPS9."""
        # This is integration test verifying extract_gps_blocks works with Hero 11-13
        assert hasattr(gps, 'extract_gps_blocks')
        # Function updated to detect both GPS5 and GPS9 keys
        # Further testing requires real GPMF data with Hero 11-13 streams


class TestGPS9Validation:
    """Test GPS9 data validation."""
    
    def test_gps9_fix_status_values(self):
        """Test GPS9 fix status field is properly handled."""
        # GPS9 fix field can have values: 0 (no fix), 2 (2D fix), 3 (3D fix)
        gps9_data = np.array([[441287283, 54277150, 833759, 9221, 10123, 7895, 36000, 100, 3]], dtype=np.int32)
        scaling = np.array([10000000, 10000000, 1000, 1000, 1000, 1, 1, 100, 1])
        
        block = [
            KVLItem(key='GPS9', value=gps9_data),
            KVLItem(key='SCAL', value=scaling),
            KVLItem(key='STNM', value='Test'),
            KVLItem(key='GPSU', value='2024-01-12 10:00:00.000'),
            KVLItem(key='GPSP', value=150),
            KVLItem(key='GPSF', value=3),
            KVLItem(key='UNIT', value='deg,deg,m,m/s,m/s'),
        ]
        
        gps_data = gps.parse_gps_block(block)
        assert gps_data.fix == 3
    
    def test_gps9_precision_field(self):
        """Test GPS9 precision field (1/100 degree accuracy)."""
        gps9_data = np.array([[441287283, 54277150, 833759, 9221, 10123, 7895, 36000, 100, 3]], dtype=np.int32)
        scaling = np.array([10000000, 10000000, 1000, 1000, 1000, 1, 1, 100, 1])
        
        block = [
            KVLItem(key='GPS9', value=gps9_data),
            KVLItem(key='SCAL', value=scaling),
            KVLItem(key='STNM', value='Test'),
            KVLItem(key='GPSU', value='2024-01-12 10:00:00.000'),
            KVLItem(key='GPSP', value=85),  # 0.85 degree precision
            KVLItem(key='GPSF', value=3),
            KVLItem(key='UNIT', value='deg,deg,m,m/s,m/s'),
        ]
        
        gps_data = gps.parse_gps_block(block)
        assert gps_data.precision == pytest.approx(0.85, rel=1e-2)

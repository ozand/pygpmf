"""Tests for gyroscope and accelerometer data extraction."""
import pytest
import numpy as np
from collections import namedtuple
from gpmf import gyro

# Mock KVLItem for testing
KVLItem = namedtuple('KVLItem', ['key', 'value'])


class TestGyroDataExtraction:
    """Test gyroscope data extraction."""
    
    @pytest.fixture
    def gyro_block(self):
        """Create a mock gyroscope block."""
        # Gyroscope: x, y, z angular velocities (rad/s)
        gyro_data = np.array([
            [100, 50, -25],    # Sample angular velocities (scaled)
            [102, 48, -26],
            [98, 52, -24],
        ], dtype=np.int16)
        
        scaling_factors = np.array([1, 1, 1])
        
        return [
            KVLItem(key='GYRO', value=gyro_data),
            KVLItem(key='SCAL', value=scaling_factors),
            KVLItem(key='STNM', value='Gyroscope'),
            KVLItem(key='GPSU', value='2024-01-12 10:00:00.000'),
            KVLItem(key='UNIT', value='rad/s'),
        ]
    
    @pytest.fixture
    def accel_block(self):
        """Create a mock accelerometer block."""
        # Accelerometer: x, y, z linear accelerations (m/s²)
        accel_data = np.array([
            [1000, 500, -250],   # Scaled accelerations
            [1020, 480, -260],
            [980, 520, -240],
        ], dtype=np.int16)
        
        scaling_factors = np.array([100, 100, 100])
        
        return [
            KVLItem(key='ACCL', value=accel_data),
            KVLItem(key='SCAL', value=scaling_factors),
            KVLItem(key='STNM', value='Accelerometer'),
            KVLItem(key='GPSU', value='2024-01-12 10:00:00.000'),
            KVLItem(key='UNIT', value='m/s²'),
        ]
    
    def test_parse_gyro_block_basic(self, gyro_block):
        """Test basic gyroscope block parsing."""
        gyro_data = gyro.parse_gyro_block(gyro_block)
        
        assert gyro_data.description == 'Gyroscope'
        assert gyro_data.timestamp == '2024-01-12 10:00:00.000'
        assert gyro_data.units == 'rad/s'
        assert gyro_data.npoints == 3
        assert len(gyro_data.x) == 3
        assert len(gyro_data.y) == 3
        assert len(gyro_data.z) == 3
    
    def test_parse_accel_block_basic(self, accel_block):
        """Test basic accelerometer block parsing."""
        accel_data = gyro.parse_accel_block(accel_block)
        
        assert accel_data.description == 'Accelerometer'
        assert accel_data.timestamp == '2024-01-12 10:00:00.000'
        assert accel_data.units == 'm/s²'
        assert accel_data.npoints == 3
        assert len(accel_data.x) == 3
        assert len(accel_data.y) == 3
        assert len(accel_data.z) == 3
    
    def test_gyro_axis_values(self, gyro_block):
        """Test gyroscope axis value extraction."""
        gyro_data = gyro.parse_gyro_block(gyro_block)
        
        # Verify first sample values
        assert gyro_data.x[0] == pytest.approx(100.0, rel=1e-6)
        assert gyro_data.y[0] == pytest.approx(50.0, rel=1e-6)
        assert gyro_data.z[0] == pytest.approx(-25.0, rel=1e-6)
    
    def test_accel_axis_values(self, accel_block):
        """Test accelerometer axis value extraction."""
        accel_data = gyro.parse_accel_block(accel_block)
        
        # With scaling factor of 100: 1000/100 = 10.0
        assert accel_data.x[0] == pytest.approx(10.0, rel=1e-6)
        assert accel_data.y[0] == pytest.approx(5.0, rel=1e-6)
        assert accel_data.z[0] == pytest.approx(-2.5, rel=1e-6)


class TestGyroDataContainers:
    """Test gyroscope and accelerometer data containers."""
    
    def test_gyro_data_namedtuple(self):
        """Test GyroData namedtuple structure."""
        gyro_data = gyro.GyroData(
            description='Test',
            timestamp='2024-01-12 10:00:00.000',
            x=np.array([1.0, 2.0]),
            y=np.array([0.5, 1.0]),
            z=np.array([-0.25, -0.5]),
            temperature=25.0,
            units='rad/s',
            npoints=2
        )
        
        assert gyro_data.description == 'Test'
        assert len(gyro_data.x) == 2
        assert gyro_data.temperature == 25.0
    
    def test_accel_data_namedtuple(self):
        """Test AccelData namedtuple structure."""
        accel_data = gyro.AccelData(
            description='Test',
            timestamp='2024-01-12 10:00:00.000',
            x=np.array([9.8, 9.9]),
            y=np.array([0.1, 0.2]),
            z=np.array([-0.05, -0.1]),
            temperature=25.0,
            units='m/s²',
            npoints=2
        )
        
        assert accel_data.description == 'Test'
        assert len(accel_data.x) == 2
        assert accel_data.temperature == 25.0


class TestGyroIntegrationPlaceholders:
    """Test placeholder implementations for future features."""
    
    def test_calculate_rotation_not_implemented(self):
        """Test that rotation calculation raises NotImplementedError."""
        gyro_data = gyro.GyroData(
            description='Test',
            timestamp='2024-01-12 10:00:00.000',
            x=np.array([0.1]),
            y=np.array([0.05]),
            z=np.array([-0.025]),
            temperature=25.0,
            units='rad/s',
            npoints=1
        )
        
        with pytest.raises(NotImplementedError):
            gyro.calculate_rotation_from_gyro(gyro_data)
    
    def test_gyroflow_export_not_implemented(self):
        """Test that GyroFlow export raises NotImplementedError."""
        gyro_data = gyro.GyroData(
            description='Test',
            timestamp='2024-01-12 10:00:00.000',
            x=np.array([0.1]),
            y=np.array([0.05]),
            z=np.array([-0.025]),
            temperature=25.0,
            units='rad/s',
            npoints=1
        )
        
        with pytest.raises(NotImplementedError):
            gyro.export_gyroflow_json(gyro_data)

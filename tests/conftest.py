"""Pytest configuration and fixtures."""
import pytest
import os
from pathlib import Path

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def sample_gpmf_stream():
    """Provide a sample GPMF binary stream for testing."""
    # Minimal valid GPMF stream (will be replaced with real data)
    return b'\x00\x00\x00\x00'


@pytest.fixture
def test_data_dir():
    """Provide path to test data directory."""
    return TEST_DATA_DIR


@pytest.fixture
def sample_gps_data():
    """Provide sample GPS data for testing."""
    return {
        'lat': 44.1287283,
        'lon': 5.427715,
        'alt': 833.759,
        'speed_2d': 9.221,
        'speed_3d': 9.25,
        'timestamp': '2020-07-03T12:36:56.940000Z'
    }

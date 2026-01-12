"""Gyroscope and accelerometer data extraction from GPMF streams.

Supports Hero 5+ models with gyro/accelerometer telemetry for video stabilization.
"""

from collections import namedtuple
import numpy as np

# Data container for gyroscope readings
GyroData = namedtuple('GyroData', [
    'description',      # Stream description
    'timestamp',        # Timestamp string
    'x', 'y', 'z',     # Angular velocity (x, y, z axes in rad/s)
    'temperature',      # Sensor temperature
    'units',            # Units string
    'npoints',          # Number of data points
])

# Data container for accelerometer readings
AccelData = namedtuple('AccelData', [
    'description',      # Stream description
    'timestamp',        # Timestamp string
    'x', 'y', 'z',     # Linear acceleration (x, y, z axes in m/s²)
    'temperature',      # Sensor temperature
    'units',            # Units string
    'npoints',          # Number of data points
])


def extract_gyro_blocks(gpmf_bytes):
    """Extract all gyroscope data blocks from GPMF stream.
    
    Gyroscope streams are typically nested in STRM containers.
    
    Parameters
    ----------
    gpmf_bytes : bytes
        Raw GPMF data bytes
    
    Yields
    ------
    gyro_block : list of KVLItem
        A list of KVLItem corresponding to a gyroscope data block
    """
    from .parse import iter_klv, KLV_LIST
    
    for elt in iter_klv(gpmf_bytes, KLV_LIST):
        if elt.key == "STRM":
            # Found a stream container, extract GYRO data
            for sub_elt in iter_klv(elt.value, KLV_LIST):
                if sub_elt.key == "GYRO":
                    # Found GYRO stream, yield the containing block
                    # Collect all items in this stream
                    block = []
                    for item in iter_klv(elt.value, KLV_LIST):
                        block.append(item)
                    if any(item.key == "GYRO" for item in block):
                        yield block
                    break


def extract_accel_blocks(gpmf_bytes):
    """Extract all accelerometer data blocks from GPMF stream.
    
    Accelerometer streams are typically nested in STRM containers.
    
    Parameters
    ----------
    gpmf_bytes : bytes
        Raw GPMF data bytes
    
    Yields
    ------
    accel_block : list of KVLItem
        A list of KVLItem corresponding to an accelerometer data block
    """
    from .parse import iter_klv, KLV_LIST
    
    for elt in iter_klv(gpmf_bytes, KLV_LIST):
        if elt.key == "STRM":
            # Found a stream container, extract ACCL data
            for sub_elt in iter_klv(elt.value, KLV_LIST):
                if sub_elt.key == "ACCL":
                    # Found ACCL stream, yield the containing block
                    block = []
                    for item in iter_klv(elt.value, KLV_LIST):
                        block.append(item)
                    if any(item.key == "ACCL" for item in block):
                        yield block
                    break


def parse_gyro_block(gyro_block):
    """Parse gyroscope data block into GyroData objects.
    
    Parameters
    ----------
    gyro_block : list of KVLItem
        A list of KVLItem corresponding to a gyroscope data block
    
    Returns
    -------
    gyro_data : GyroData
        A GyroData object holding the gyroscope information
    """
    block_dict = {s.key: s for s in gyro_block}
    
    # Extract gyro values and scale
    gyro_values = block_dict["GYRO"].value * 1.0 / block_dict["SCAL"].value
    
    # Unpack x, y, z axes
    if hasattr(gyro_values, 'T'):
        x, y, z = gyro_values.T
    else:
        x, y, z = gyro_values
    
    # Extract temperature if available (optional)
    temperature = None
    if "TMPC" in block_dict:
        temperature = block_dict["TMPC"].value
    
    return GyroData(
        description=block_dict.get("STNM", namedtuple('Item', ['value'])("Gyroscope")).value,
        timestamp=block_dict.get("GPSU", namedtuple('Item', ['value'])("")).value,
        x=x,
        y=y,
        z=z,
        temperature=temperature,
        units=block_dict.get("UNIT", namedtuple('Item', ['value'])("rad/s")).value,
        npoints=len(gyro_values) if hasattr(gyro_values, '__len__') else 1
    )


def parse_accel_block(accel_block):
    """Parse accelerometer data block into AccelData objects.
    
    Parameters
    ----------
    accel_block : list of KVLItem
        A list of KVLItem corresponding to an accelerometer data block
    
    Returns
    -------
    accel_data : AccelData
        An AccelData object holding the accelerometer information
    """
    block_dict = {s.key: s for s in accel_block}
    
    # Extract acceleration values and scale
    accel_values = block_dict["ACCL"].value * 1.0 / block_dict["SCAL"].value
    
    # Unpack x, y, z axes
    if hasattr(accel_values, 'T'):
        x, y, z = accel_values.T
    else:
        x, y, z = accel_values
    
    # Extract temperature if available (optional)
    temperature = None
    if "TMPC" in block_dict:
        temperature = block_dict["TMPC"].value
    
    return AccelData(
        description=block_dict.get("STNM", namedtuple('Item', ['value'])("Accelerometer")).value,
        timestamp=block_dict.get("GPSU", namedtuple('Item', ['value'])("")).value,
        x=x,
        y=y,
        z=z,
        temperature=temperature,
        units=block_dict.get("UNIT", namedtuple('Item', ['value'])("m/s²")).value,
        npoints=len(accel_values) if hasattr(accel_values, '__len__') else 1
    )


def calculate_rotation_from_gyro(gyro_data, sample_rate=None):
    """Calculate cumulative rotation from gyroscope data using integration.
    
    Parameters
    ----------
    gyro_data : GyroData
        Gyroscope data from parse_gyro_block()
    sample_rate : float, optional
        Sample rate in Hz. If None, assumes uniform spacing
    
    Returns
    -------
    rotations : tuple of arrays
        (roll, pitch, yaw) rotation angles in degrees
    """
    # Placeholder for future integration
    # Would need proper integration method (e.g., Runge-Kutta)
    raise NotImplementedError("Gyro integration for stabilization coming in v0.4.0")


def export_gyroflow_json(gyro_data, accel_data=None, output_path=None):
    """Export gyroscope data in GyroFlow JSON format.
    
    GyroFlow format for video stabilization with gyroscope telemetry.
    
    Parameters
    ----------
    gyro_data : GyroData or list of GyroData
        Gyroscope data from parse_gyro_block()
    accel_data : AccelData or list of AccelData, optional
        Accelerometer data from parse_accel_block()
    output_path : str, optional
        Output file path. If None, returns dict
    
    Returns
    -------
    gyroflow_dict : dict
        GyroFlow-compatible dictionary, or None if saved to file
    """
    # Placeholder for GyroFlow integration
    # Will implement JSON export matching GyroFlow specification
    raise NotImplementedError("GyroFlow export planned for v0.4.0")

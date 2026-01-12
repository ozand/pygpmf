#!/usr/bin/env python3
"""Example: Extract and analyze gyroscope/accelerometer data.

This example demonstrates how to use pygpmf_oz to extract gyroscope
and accelerometer telemetry from GoPro videos (Hero 5+).

Gyroscope & Accelerometer Features:
- GYRO: 3-axis angular velocity (rad/s) at high frequency
- ACCL: 3-axis linear acceleration (m/s²) at high frequency
- Temperature: Sensor temperature monitoring
- Foundation for video stabilization (GyroFlow integration)

Requirements:
- pygpmf_oz v0.3.0+
- GoPro video file (Hero 5+ with gyro/accel telemetry)

Usage:
    python example_gyro_extract.py <video_file.mp4>

Notes:
- Gyroscope/accelerometer data enables GyroFlow stabilization
- Typically recorded at 200Hz for modern GoPro models
- Raw angular velocities and accelerations need calibration
- Future versions will include IMU integration and stabilization export
"""

import argparse
import sys
from gpmf import parse, gyro


def extract_gyro_data(video_file):
    """Extract and display gyroscope and accelerometer data.
    
    Parameters
    ----------
    video_file : str
        Path to GoPro video file
    """
    print(f"Reading GPMF data from: {video_file}")
    
    try:
        # Read GPMF payload from video
        gpmf_bytes = parse.extract_gpmf(video_file)
        if not gpmf_bytes:
            print("No GPMF data found in video file.")
            return
        
        print(f"GPMF payload size: {len(gpmf_bytes)} bytes\n")
        
        # Extract gyroscope blocks
        gyro_blocks = list(gyro.extract_gyro_blocks(gpmf_bytes))
        print(f"Found {len(gyro_blocks)} gyroscope data blocks")
        
        # Extract accelerometer blocks
        accel_blocks = list(gyro.extract_accel_blocks(gpmf_bytes))
        print(f"Found {len(accel_blocks)} accelerometer data blocks\n")
        
        # Process gyroscope data
        if gyro_blocks:
            print("=" * 60)
            print("GYROSCOPE DATA")
            print("=" * 60)
            
            for i, block in enumerate(gyro_blocks, 1):
                try:
                    gyro_data = gyro.parse_gyro_block(block)
                    
                    print(f"\nGyroscope Block #{i}")
                    print(f"  Description: {gyro_data.description}")
                    print(f"  Timestamp: {gyro_data.timestamp}")
                    print(f"  Units: {gyro_data.units}")
                    print(f"  Data points: {gyro_data.npoints}")
                    
                    if gyro_data.npoints > 0:
                        print(f"  First reading:")
                        print(f"    X (roll): {gyro_data.x[0]:.6f} rad/s")
                        print(f"    Y (pitch): {gyro_data.y[0]:.6f} rad/s")
                        print(f"    Z (yaw): {gyro_data.z[0]:.6f} rad/s")
                        
                        if gyro_data.temperature is not None:
                            print(f"  Temperature: {gyro_data.temperature:.1f}°C")
                        
                        # Show statistics
                        import numpy as np
                        print(f"  X range: {np.min(gyro_data.x):.6f} to {np.max(gyro_data.x):.6f} rad/s")
                        print(f"  Y range: {np.min(gyro_data.y):.6f} to {np.max(gyro_data.y):.6f} rad/s")
                        print(f"  Z range: {np.min(gyro_data.z):.6f} to {np.max(gyro_data.z):.6f} rad/s")
                
                except KeyError as e:
                    print(f"  Error parsing gyroscope block: Missing field {e}")
                except Exception as e:
                    print(f"  Error parsing gyroscope block: {e}")
        
        # Process accelerometer data
        if accel_blocks:
            print("\n" + "=" * 60)
            print("ACCELEROMETER DATA")
            print("=" * 60)
            
            for i, block in enumerate(accel_blocks, 1):
                try:
                    accel_data = gyro.parse_accel_block(block)
                    
                    print(f"\nAccelerometer Block #{i}")
                    print(f"  Description: {accel_data.description}")
                    print(f"  Timestamp: {accel_data.timestamp}")
                    print(f"  Units: {accel_data.units}")
                    print(f"  Data points: {accel_data.npoints}")
                    
                    if accel_data.npoints > 0:
                        print(f"  First reading:")
                        print(f"    X (lateral): {accel_data.x[0]:.6f} m/s²")
                        print(f"    Y (forward): {accel_data.y[0]:.6f} m/s²")
                        print(f"    Z (vertical): {accel_data.z[0]:.6f} m/s²")
                        
                        if accel_data.temperature is not None:
                            print(f"  Temperature: {accel_data.temperature:.1f}°C")
                        
                        # Show statistics
                        import numpy as np
                        print(f"  X range: {np.min(accel_data.x):.6f} to {np.max(accel_data.x):.6f} m/s²")
                        print(f"  Y range: {np.min(accel_data.y):.6f} to {np.max(accel_data.y):.6f} m/s²")
                        print(f"  Z range: {np.min(accel_data.z):.6f} to {np.max(accel_data.z):.6f} m/s²")
                
                except KeyError as e:
                    print(f"  Error parsing accelerometer block: Missing field {e}")
                except Exception as e:
                    print(f"  Error parsing accelerometer block: {e}")
        
        if not gyro_blocks and not accel_blocks:
            print("No gyroscope or accelerometer data found in video.")
            print("\nNote: Not all GoPro models include IMU telemetry.")
            print("Gyroscope/accelerometer is available on:")
            print("  - Hero 5 and later")
            print("  - Some action-specific models (Hero Max, etc.)")
        
        print("\n" + "=" * 60)
        print("Future Enhancements (v0.4.0+):")
        print("  - IMU rotation integration for orientation tracking")
        print("  - GyroFlow JSON export for video stabilization")
        print("  - Sensor calibration and bias correction")
        print("=" * 60)
    
    except FileNotFoundError:
        print(f"Error: File not found: {video_file}")
    except Exception as e:
        print(f"Error processing video: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract gyroscope and accelerometer data from GoPro video"
    )
    parser.add_argument(
        'video_file',
        help='GoPro video file (MP4 or MOV)'
    )
    
    args = parser.parse_args()
    extract_gyro_data(args.video_file)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Example: Extract and analyze Hero 11-13 GPS9 data.

This example demonstrates how to use pygpmf_oz to extract and analyze
GPS9 telemetry from GoPro Hero 11, 12, and 13 cameras.

Hero 11-13 GPS Features:
- GPS9: 10Hz high-frequency GPS with 9 fields (vs GPS5's 5 fields)
- Enhanced precision with Dilution of Precision (DOP)
- Accurate fix status (2D/3D)
- Compatible with Hero 5-10 (falls back to GPS5 if present)

Requirements:
- pygpmf_oz v0.3.0+
- GoPro video file (Hero 11/12/13 GPMF format)

Usage:
    python example_gps9_extract.py <video_file.mp4>
"""

import argparse
import sys
from gpmf import parse, gps


def extract_gps9_data(video_file):
    """Extract and display Hero 11-13 GPS9 data.
    
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
        
        # Extract GPS blocks (auto-detects GPS5 or GPS9)
        gps_blocks = list(gps.extract_gps_blocks(gpmf_bytes))
        print(f"Found {len(gps_blocks)} GPS data blocks\n")
        
        if not gps_blocks:
            print("No GPS data found.")
            return
        
        # Parse and display GPS data
        for i, block in enumerate(gps_blocks, 1):
            try:
                gps_data = gps.parse_gps_block(block)
                
                print(f"GPS Block #{i}")
                print(f"  Description: {gps_data.description}")
                print(f"  Timestamp: {gps_data.timestamp}")
                print(f"  Precision: {gps_data.precision:.2f}°")
                print(f"  Fix: {gps.FIX_TYPE.get(gps_data.fix, f'Unknown ({gps_data.fix})')}")
                print(f"  Data points: {gps_data.npoints}")
                print(f"  Coordinates: {len(gps_data.latitude)} samples")
                
                if len(gps_data.latitude) > 0:
                    # Show first coordinate
                    print(f"  First point: {gps_data.latitude[0]:.6f}, {gps_data.longitude[0]:.6f}")
                    print(f"  Altitude: {gps_data.altitude[0]:.1f}m")
                    print(f"  Speed (2D): {gps_data.speed_2d[0]:.2f} m/s")
                    print(f"  Speed (3D): {gps_data.speed_3d[0]:.2f} m/s")
                    
                    # Show statistics
                    import numpy as np
                    print(f"  Lat range: {np.min(gps_data.latitude):.6f} to {np.max(gps_data.latitude):.6f}")
                    print(f"  Lon range: {np.min(gps_data.longitude):.6f} to {np.max(gps_data.longitude):.6f}")
                    print(f"  Alt range: {np.min(gps_data.altitude):.1f} to {np.max(gps_data.altitude):.1f}m")
                    print(f"  Max speed: {np.max(gps_data.speed_2d):.2f} m/s")
                
                print()
                
            except KeyError as e:
                print(f"  Error parsing GPS block: Missing field {e}")
                print()
                continue
        
        # Generate GPX track if all data present
        try:
            gpx_segment = gps.make_pgx_segment(gps_blocks)
            if gpx_segment:
                print(f"Generated GPX segment with {len(gpx_segment.points)} points")
                
                # Save GPX file
                output_file = video_file.replace('.mp4', '.gpx').replace('.mov', '.gpx')
                gpx_segment.save(output_file)
                print(f"✓ Saved GPX track to: {output_file}")
        except Exception as e:
            print(f"Could not generate GPX track: {e}")
    
    except FileNotFoundError:
        print(f"Error: File not found: {video_file}")
    except Exception as e:
        print(f"Error processing video: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract Hero 11-13 GPS9 data from GoPro video"
    )
    parser.add_argument(
        'video_file',
        help='GoPro video file (MP4 or MOV)'
    )
    
    args = parser.parse_args()
    extract_gps9_data(args.video_file)


if __name__ == '__main__':
    main()

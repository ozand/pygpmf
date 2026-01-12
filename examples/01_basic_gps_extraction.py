#!/usr/bin/env python
"""
Example 1: Basic GPS Extraction from GoPro Video

This example demonstrates how to:
1. Extract GPMF stream from a GoPro MP4 file
2. Parse GPS data
3. Print GPS coordinates

Requirements:
    - GoPro video file with GPS data
    - FFmpeg installed on your system
"""

import gpmf

# Path to your GoPro video file
VIDEO_FILE = 'GOPR0001.MP4'

def main():
    print("=" * 60)
    print("Example 1: Basic GPS Extraction")
    print("=" * 60)
    
    # Step 1: Extract GPMF binary stream from video
    print("\n[1/3] Extracting GPMF stream from video...")
    try:
        stream = gpmf.io.extract_gpmf_stream(VIDEO_FILE)
        print(f"✓ Extracted {len(stream)} bytes of GPMF data")
    except Exception as e:
        print(f"✗ Error extracting stream: {e}")
        print("\nMake sure:")
        print("  - Video file exists")
        print("  - FFmpeg is installed")
        print("  - Video contains GPMF metadata")
        return
    
    # Step 2: Extract GPS blocks from stream
    print("\n[2/3] Parsing GPS blocks...")
    try:
        gps_blocks = gpmf.gps.extract_gps_blocks(stream)
        print(f"✓ Found {len(gps_blocks)} GPS blocks")
    except Exception as e:
        print(f"✗ Error parsing GPS: {e}")
        return
    
    # Step 3: Parse GPS data
    print("\n[3/3] Processing GPS data...")
    gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))
    
    if not gps_data:
        print("✗ No GPS data found in video")
        print("\nPossible reasons:")
        print("  - GPS was disabled during recording")
        print("  - Camera was indoors (no GPS fix)")
        print("  - Older GoPro model without GPS")
        return
    
    print(f"✓ Parsed {len(gps_data)} GPS points")
    
    # Display first 5 GPS points
    print("\n" + "=" * 60)
    print("First 5 GPS Points:")
    print("=" * 60)
    
    for i, point in enumerate(gps_data[:5], 1):
        print(f"\nPoint {i}:")
        print(f"  Latitude:    {point.get('lat', 'N/A'):.6f}°")
        print(f"  Longitude:   {point.get('lon', 'N/A'):.6f}°")
        print(f"  Altitude:    {point.get('alt', 'N/A'):.1f} m")
        print(f"  Speed (2D):  {point.get('speed_2d', 0):.2f} m/s")
        print(f"  Timestamp:   {point.get('timestamp', 'N/A')}")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("Summary Statistics:")
    print("=" * 60)
    
    latitudes = [p.get('lat') for p in gps_data if p.get('lat')]
    longitudes = [p.get('lon') for p in gps_data if p.get('lon')]
    altitudes = [p.get('alt') for p in gps_data if p.get('alt')]
    speeds = [p.get('speed_2d', 0) for p in gps_data]
    
    if latitudes and longitudes:
        print(f"\nTotal GPS points:  {len(gps_data)}")
        print(f"Latitude range:    {min(latitudes):.6f}° to {max(latitudes):.6f}°")
        print(f"Longitude range:   {min(longitudes):.6f}° to {max(longitudes):.6f}°")
        
        if altitudes:
            print(f"Altitude range:    {min(altitudes):.1f} m to {max(altitudes):.1f} m")
        
        if speeds:
            print(f"Max speed:         {max(speeds):.2f} m/s ({max(speeds) * 3.6:.1f} km/h)")
    
    print("\n✓ Done!")


if __name__ == '__main__':
    main()

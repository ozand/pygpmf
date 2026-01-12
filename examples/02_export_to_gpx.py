#!/usr/bin/env python
"""
Example 2: Export GPS Track to GPX Format

This example demonstrates how to:
1. Extract GPS data from GoPro video
2. Convert to GPX format
3. Save GPX file for use in mapping applications

GPX files can be imported into:
    - Google Earth
    - Strava
    - Garmin Connect
    - MapMyRide
    - And many other GPS applications
"""

import gpmf
import gpxpy
import gpxpy.gpx
from datetime import datetime

# Configuration
VIDEO_FILE = 'GOPR0001.MP4'
OUTPUT_GPX = 'track.gpx'

def main():
    print("=" * 60)
    print("Example 2: Export to GPX Format")
    print("=" * 60)
    
    # Extract GPMF stream
    print("\n[1/4] Extracting GPMF stream...")
    try:
        stream = gpmf.io.extract_gpmf_stream(VIDEO_FILE)
        print(f"✓ Extracted {len(stream)} bytes")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Extract and parse GPS
    print("\n[2/4] Parsing GPS data...")
    try:
        gps_blocks = gpmf.gps.extract_gps_blocks(stream)
        gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))
        print(f"✓ Parsed {len(gps_data)} GPS points")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    if not gps_data:
        print("✗ No GPS data found")
        return
    
    # Create GPX structure
    print("\n[3/4] Creating GPX structure...")
    gpx = gpxpy.gpx.GPX()
    
    # Add metadata
    gpx.creator = "pygpmf-oz v0.2.0"
    gpx.name = f"GoPro Track - {datetime.now().strftime('%Y-%m-%d')}"
    gpx.description = f"GPS track extracted from {VIDEO_FILE}"
    
    # Create track
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_track.name = "GoPro GPS Track"
    gpx.tracks.append(gpx_track)
    
    # Create segment and add points
    gpx_segment = gpmf.gps.make_gpx_segment(gps_data)
    gpx_track.segments.append(gpx_segment)
    
    print(f"✓ Created GPX with {len(gpx_segment.points)} points")
    
    # Save GPX file
    print(f"\n[4/4] Saving to {OUTPUT_GPX}...")
    try:
        with open(OUTPUT_GPX, 'w', encoding='utf-8') as f:
            f.write(gpx.to_xml())
        print(f"✓ Saved GPX file")
    except Exception as e:
        print(f"✗ Error saving: {e}")
        return
    
    # Display GPX statistics
    print("\n" + "=" * 60)
    print("GPX Statistics:")
    print("=" * 60)
    
    # Calculate statistics using gpxpy
    moving_data = gpx.get_moving_data()
    uphill_downhill = gpx.get_uphill_downhill()
    
    if moving_data:
        print(f"\nMoving time:       {moving_data.moving_time / 60:.1f} minutes")
        print(f"Stopped time:      {moving_data.stopped_time / 60:.1f} minutes")
        print(f"Moving distance:   {moving_data.moving_distance / 1000:.2f} km")
        print(f"Max speed:         {moving_data.max_speed * 3.6:.1f} km/h")
    
    if uphill_downhill:
        print(f"\nElevation gain:    {uphill_downhill.uphill:.1f} m")
        print(f"Elevation loss:    {uphill_downhill.downhill:.1f} m")
    
    # Bounds
    bounds = gpx.get_bounds()
    if bounds:
        print(f"\nBounds:")
        print(f"  North: {bounds.max_latitude:.6f}°")
        print(f"  South: {bounds.min_latitude:.6f}°")
        print(f"  East:  {bounds.max_longitude:.6f}°")
        print(f"  West:  {bounds.min_longitude:.6f}°")
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("=" * 60)
    print(f"\n1. Open {OUTPUT_GPX} in Google Earth")
    print("2. Upload to Strava or Garmin Connect")
    print("3. View in any GPX-compatible mapping software")
    print("\n✓ Done!")


if __name__ == '__main__':
    main()

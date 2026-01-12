#!/usr/bin/env python
"""
Example 3: Visualize GPS Track on Map

This example demonstrates how to:
1. Extract GPS data from GoPro video
2. Create a visual map with the GPS track
3. Save as an HTML file or PNG image

Requirements:
    - geopandas
    - matplotlib
    - contextily (for map tiles)
"""

import gpmf

# Configuration
VIDEO_FILE = 'GOPR0001.MP4'
OUTPUT_PNG = 'gps_track.png'
OUTPUT_HTML = 'gps_track.html'

def main():
    print("=" * 60)
    print("Example 3: Visualize GPS Track")
    print("=" * 60)
    
    # Extract GPMF stream
    print("\n[1/3] Extracting GPS data...")
    try:
        stream = gpmf.io.extract_gpmf_stream(VIDEO_FILE)
        print(f"✓ Extracted {len(stream)} bytes")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Create visualization
    print("\n[2/3] Creating map visualization...")
    try:
        gpmf.gps_plot.plot_gps_trace_from_stream(stream)
        print("✓ Map created")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nInstall required packages:")
        print("  pip install geopandas matplotlib contextily")
        return
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    print("\n[3/3] Saving visualization...")
    print(f"✓ Saved to {OUTPUT_PNG}")
    
    print("\n" + "=" * 60)
    print("Map Features:")
    print("=" * 60)
    print("\n- GPS track displayed on OpenStreetMap tiles")
    print("- Start point marked in green")
    print("- End point marked in red")
    print("- Track colored by speed (if available)")
    
    print("\n✓ Done! Open the image to view your GPS track.")


if __name__ == '__main__':
    main()

"""Example: Extract and print GPS statistics"""

import sys
from pathlib import Path
from gpmf import parse_file, gps
import json

def extract_gps_stats(video_file: str):
    \"\"\"Extract GPS data and show statistics\"\"\"
    
    video_path = Path(video_file)
    if not video_path.exists():
        print(f\"❌ File not found: {video_file}\")
        return False
    
    try:
        print(f\"📹 Parsing GPMF from: {video_file}\")
        data = parse_file(str(video_path))
        
        print(f\"📍 Extracting GPS data...\")
        gps_data = gps.extract_gps(data)
        
        if not gps_data:
            print(\"❌ No GPS data found in video\")
            return False
        
        print(f\"✅ Found {len(gps_data)} GPS points\\n\")
        
        # Calculate statistics
        latitudes = [p.latitude for p in gps_data if p.latitude is not None]
        longitudes = [p.longitude for p in gps_data if p.longitude is not None]
        altitudes = [p.altitude for p in gps_data if p.altitude is not None]
        speeds = [p.speed_2d for p in gps_data if p.speed_2d is not None]
        
        stats = {
            'total_points': len(gps_data),
            'latitude': {
                'min': min(latitudes) if latitudes else None,
                'max': max(latitudes) if latitudes else None,
                'avg': sum(latitudes) / len(latitudes) if latitudes else None,
            },
            'longitude': {
                'min': min(longitudes) if longitudes else None,
                'max': max(longitudes) if longitudes else None,
                'avg': sum(longitudes) / len(longitudes) if longitudes else None,
            },
            'altitude': {
                'min': min(altitudes) if altitudes else None,
                'max': max(altitudes) if altitudes else None,
                'avg': sum(altitudes) / len(altitudes) if altitudes else None,
            },
            'speed_2d': {
                'min': min(speeds) if speeds else None,
                'max': max(speeds) if speeds else None,
                'avg': sum(speeds) / len(speeds) if speeds else None,
            },
        }
        
        print(\"📊 GPS Statistics:\")
        print(f\"  Total points: {stats['total_points']}\")
        print(f\"  Latitude:  {stats['latitude']['avg']:.6f} (min: {stats['latitude']['min']:.6f}, max: {stats['latitude']['max']:.6f})\")
        print(f\"  Longitude: {stats['longitude']['avg']:.6f} (min: {stats['longitude']['min']:.6f}, max: {stats['longitude']['max']:.6f})\")
        print(f\"  Altitude:  {stats['altitude']['avg']:.1f}m (min: {stats['altitude']['min']:.1f}m, max: {stats['altitude']['max']:.1f}m)\")
        print(f\"  Speed 2D:  {stats['speed_2d']['avg']:.2f} m/s (min: {stats['speed_2d']['min']:.2f}, max: {stats['speed_2d']['max']:.2f})\")
        
        return True
        
    except Exception as e:
        print(f\"❌ Error: {e}\")
        import traceback
        traceback.print_exc()
        return False

if __name__ == \"__main__\":
    if len(sys.argv) < 2:
        print(\"Usage: python example_gps_stats.py <video_file>\")
        print()
        print(\"Example:\")
        print(\"  python example_gps_stats.py GOPR0001.MP4\")
        sys.exit(1)
    
    video = sys.argv[1]
    extract_gps_stats(video)

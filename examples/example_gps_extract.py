"""Example: Extract GPS data and save to GPX"""

import sys
from pathlib import Path
from gpmf import parse_file, gps

def extract_gps_to_gpx(video_file: str, output_file: str = None):
    """Extract GPS data from GoPro video and save as GPX"""
    
    video_path = Path(video_file)
    if not video_path.exists():
        print(f"❌ File not found: {video_file}")
        return False
    
    if output_file is None:
        output_file = video_path.stem + ".gpx"
    
    try:
        print(f"📹 Parsing GPMF from: {video_file}")
        data = parse_file(str(video_path))
        
        print(f"📍 Extracting GPS data...")
        gps_data = gps.extract_gps(data)
        
        if not gps_data:
            print("❌ No GPS data found in video")
            return False
        
        print(f"✅ Found {len(gps_data)} GPS points")
        
        # Create GPX document
        gpx_doc = gps.make_gpx(gps_data)
        
        # Save to file
        with open(output_file, 'w') as f:
            f.write(gpx_doc.to_xml())
        
        print(f"💾 GPX saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python example_gps_extract.py <video_file> [output.gpx]")
        print()
        print("Example:")
        print("  python example_gps_extract.py GOPR0001.MP4")
        print("  python example_gps_extract.py GOPR0001.MP4 my_track.gpx")
        sys.exit(1)
    
    video = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    extract_gps_to_gpx(video, output)

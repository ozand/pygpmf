"""Example: Visualize GPS track on map"""

import sys
from pathlib import Path
from gpmf import parse_file, gps, gps_plot

def plot_gps_track(video_file: str, output_file: str = None):
    """Extract GPS data and plot on map"""
    
    video_path = Path(video_file)
    if not video_path.exists():
        print(f"❌ File not found: {video_file}")
        return False
    
    try:
        print(f"📹 Parsing GPMF from: {video_file}")
        data = parse_file(str(video_path))
        
        print(f"📍 Extracting GPS data...")
        gps_data = gps.extract_gps(data)
        
        if not gps_data:
            print("❌ No GPS data found in video")
            return False
        
        print(f"✅ Found {len(gps_data)} GPS points")
        print(f"🗺️  Plotting GPS track...")
        
        # Plot GPS track
        gps_plot.plot_gps_trace_from_stream(data)
        
        if output_file:
            import matplotlib.pyplot as plt
            print(f"💾 Saving plot to: {output_file}")
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
        else:
            import matplotlib.pyplot as plt
            plt.show()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python example_gps_plot.py <video_file> [output.png]")
        print()
        print("Example:")
        print("  python example_gps_plot.py GOPR0001.MP4")
        print("  python example_gps_plot.py GOPR0001.MP4 track.png")
        sys.exit(1)
    
    video = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    plot_gps_track(video, output)

"""Example: Parse raw GPMF stream"""

import sys
from pathlib import Path
from gpmf import parse_file, parse

def analyze_gpmf_stream(video_file: str):
    \"\"\"Parse and analyze raw GPMF stream structure\"\"\"
    
    video_path = Path(video_file)
    if not video_path.exists():
        print(f\"❌ File not found: {video_file}\")
        return False
    
    try:
        print(f\"📹 Parsing GPMF from: {video_file}\\n\")
        data = parse_file(str(video_path))
        
        if not data:
            print(\"❌ No GPMF data found\")
            return False
        
        print(\"📊 GPMF Stream Structure:\\n\")
        
        # Show top-level keys
        if isinstance(data, dict):
            for key, value in list(data.items())[:10]:
                value_type = type(value).__name__
                if isinstance(value, (list, tuple)):
                    print(f\"  {key}: {value_type} ({len(value)} items)\")
                elif isinstance(value, dict):
                    print(f\"  {key}: {value_type} ({len(value)} keys)\")
                else:
                    print(f\"  {key}: {value_type}\")
        
        print(f\"\\n✅ Successfully parsed GPMF stream\")
        return True
        
    except Exception as e:
        print(f\"❌ Error: {e}\")
        import traceback
        traceback.print_exc()
        return False

if __name__ == \"__main__\":
    if len(sys.argv) < 2:
        print(\"Usage: python example_raw_parse.py <video_file>\")
        print()
        print(\"Example:\")
        print(\"  python example_raw_parse.py GOPR0001.MP4\")
        sys.exit(1)
    
    video = sys.argv[1]
    analyze_gpmf_stream(video)

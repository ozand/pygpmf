# pygpmf-oz Examples

This directory contains example scripts demonstrating how to use pygpmf-oz.

## 📚 Available Examples

### 01_basic_gps_extraction.py
**Extract GPS coordinates from GoPro video**

```bash
python 01_basic_gps_extraction.py
```

What it does:
- Extracts GPMF stream from MP4
- Parses GPS coordinates
- Displays latitude, longitude, altitude, speed
- Shows summary statistics

Perfect for: First-time users, basic GPS extraction

---

### 02_export_to_gpx.py
**Export GPS track to GPX format**

```bash
python 02_export_to_gpx.py
```

What it does:
- Extracts GPS data
- Converts to GPX format
- Saves file compatible with Strava, Garmin, Google Earth
- Calculates distance, elevation, speed statistics

Perfect for: Athletes, fitness tracking, importing to other apps

---

### 03_visualize_gps_track.py
**Create visual map of GPS track**

```bash
python 03_visualize_gps_track.py
```

What it does:
- Extracts GPS data
- Plots track on OpenStreetMap
- Colors by speed
- Saves PNG image

Perfect for: Visualization, presentations, social media

---

## 🚀 Quick Start

### 1. Install pygpmf-oz

```bash
pip install pygpmf-oz
```

### 2. Prepare your GoPro video

Make sure you have:
- GoPro MP4 video file with GPS metadata
- FFmpeg installed on your system

### 3. Run an example

```bash
# Change VIDEO_FILE path in the script
python examples/01_basic_gps_extraction.py
```

---

## 📋 Requirements

### Required
- Python 3.9+
- pygpmf-oz
- FFmpeg

### Optional (for visualization)
- geopandas
- matplotlib
- contextily

Install all optional dependencies:
```bash
pip install pygpmf-oz[viz]
```

---

## 🎓 Learning Path

**Beginner**: Start with Example 1  
→ Understand basic GPS extraction

**Intermediate**: Try Example 2  
→ Learn GPX export for Strava/Garmin

**Advanced**: Explore Example 3  
→ Create custom visualizations

---

## 🛠️ Customization

### Change video file
```python
VIDEO_FILE = '/path/to/your/GOPR0001.MP4'
```

### Change output files
```python
OUTPUT_GPX = 'my_track.gpx'
OUTPUT_PNG = 'my_map.png'
```

### Filter by speed
```python
# Only points where speed > 10 km/h
fast_points = [p for p in gps_data if p.get('speed_2d', 0) * 3.6 > 10]
```

### Calculate distance
```python
from geopy.distance import geodesic

total_distance = 0
for i in range(len(gps_data) - 1):
    p1 = (gps_data[i]['lat'], gps_data[i]['lon'])
    p2 = (gps_data[i+1]['lat'], gps_data[i+1]['lon'])
    total_distance += geodesic(p1, p2).kilometers

print(f"Total distance: {total_distance:.2f} km")
```

---

## 🔧 Troubleshooting

### "FFmpeg not found"
**Solution**: Install FFmpeg
- Windows: `choco install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

### "No GPS data found"
**Possible reasons**:
- GPS was disabled during recording
- Camera was indoors (no GPS fix)
- Older GoPro model without GPS
- Video file is corrupted

### "Module not found"
**Solution**: Install missing dependencies
```bash
pip install geopandas matplotlib contextily
```

---

## 📖 More Examples Coming Soon

- **04_analyze_trip_statistics.py** - Calculate distance, speed, elevation
- **05_create_speed_overlay.py** - Add telemetry overlay to video
- **06_export_to_csv.py** - Export all telemetry to CSV
- **07_gyroscope_analysis.py** - Analyze gyroscope data
- **08_compare_multiple_tracks.py** - Compare GPS tracks from multiple videos

---

## 🤝 Contributing Examples

Have a cool example? Share it!

1. Create your example script
2. Add documentation
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## 📚 Additional Resources

- **Documentation**: [DEVELOPMENT_ROADMAP.md](../DEVELOPMENT_ROADMAP.md)
- **API Reference**: Coming soon
- **Video Tutorials**: Coming soon
- **GitHub Discussions**: Ask questions

---

**Need help?** Open an [issue](https://github.com/ozand/pygpmf/issues) or [discussion](https://github.com/ozand/pygpmf/discussions)

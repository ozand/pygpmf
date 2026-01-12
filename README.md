# pygpmf-oz

> **Modernized Python library for extracting and analyzing GoPro GPMF (telemetry) data**  
> Supports Python 3.9-3.13 | Windows, Linux, macOS | Active Development 2026

[![PyPI version](https://badge.fury.io/py/pygpmf-oz.svg)](https://pypi.org/project/pygpmf-oz/)
[![Python versions](https://img.shields.io/pypi/pyversions/pygpmf-oz.svg)](https://pypi.org/project/pygpmf-oz/)
[![Documentation Status](https://readthedocs.org/projects/pygpmf-oz/badge/?version=latest)](https://pygpmf-oz.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Test Coverage](https://img.shields.io/badge/coverage-79.51%25-brightgreen)](htmlcov/index.html)

---

## 🚀 What's New in v0.3.0

- ✅ **Hero 11-13 GPS9 support** (10Hz GPS with 9 fields: lat/lon/alt/speed2d/speed3d/days/secs/dop/fix)
- ✅ **Gyroscope & Accelerometer module** - Extract IMU data for video stabilization
- ✅ **134 tests passing** - Comprehensive test coverage for GPS9 and gyro functionality
- ✅ **Full backward compatibility** - GPS5 (Hero 5-10) continues to work seamlessly
- ✅ **UTF-8 FourCC fix** - Resolves decode errors in GPMF stream parsing

📖 **Documentation**: [pygpmf-oz.readthedocs.io](https://pygpmf-oz.readthedocs.io/)  
📋 **Full roadmap**: [docs/development/DEVELOPMENT_ROADMAP.md](docs/development/DEVELOPMENT_ROADMAP.md)  
📚 **All Documentation**: [docs/](docs/)

---

## 📦 Installation

```bash
pip install pygpmf-oz
```

For development:
```bash
git clone https://github.com/ozand/pygpmf-oz.git
cd pygpmf-oz
pip install -e .
```

---

## 🎯 Quick Start

A python Module to extract GPMF information from GoPro videos.

More information on the format is available on the
[GoPro GitHub page](https://github.com/gopro/gpmf-parser).

The primary aim of this project is to extract GPS tracks and sensor data
from GoPro video files. We use `ffmpeg-python` to extract the GPMF stream from video files.

```python
import gpmf

# Read the binary stream from the file
stream = gpmf.io.extract_gpmf_stream(my_file)

# Extract GPS low level data from the stream
gps_blocks = gpmf.gps.extract_gps_blocks(stream)

# Parse low level data into more usable format
gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))
```

We rely on `gpxpy` to easily convert GPS data into GPX segments:  

```python
import gpxpy

gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
gpx_track.segments.append(gpmf.gps.make_pgx_segment(gps_data))

print(gpx.to_xml())
```
```
<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
  <trk>
    <trkseg>
      <trkpt lat="44.1287283" lon="5.427715">
        <ele>833.759</ele>
        <time>2020-07-03T12:36:56.940000Z</time>
        <sym>Square</sym>
        <fix>3d</fix>
        <pdop>1.82</pdop>
        <extensions>
          <speed_2d>
            <value>9.221</value>
            <unit>m/s</unit>
          </speed_2d>
          <speed_3d>
            <value>9.25</value>
            <unit>m/s</unit>
          </speed_3d>
        </extensions>
      </trkpt>
      ...
    </trkseg>
  </trk>
</gpx>
```

You can also make an image from you gps track:

```python
import gpmf

# Read the binary stream from the file
stream = gpmf.io.extract_gpmf_stream(my_file)
gpmf.gps_plot.plot_gps_trace_from_stream(stream)
```

![GPS Track Image](./images/GH010215.png)

---

## 🎓 Use Cases

### 🚴 Sports & Fitness
- Extract GPS tracks for training analysis
- Export to GPX for Strava/Garmin compatibility
- Analyze speed, elevation, distance

### 🎬 Video Production
- Sync telemetry overlays with video
- Create data visualizations for dashboards
- Export metadata for After Effects

### 🔬 Research & Analysis
- Scientific motion studies
- Vehicle telemetry analysis
- ML training data extraction

### 🎮 FPV & Action Sports
- Video stabilization with GyroFlow (coming Q2 2026)
- G-force analysis
- Jump/trick detection

---

## 🗺️ Development Roadmap

### Q1 2026: Stabilization & Documentation ⚡
- [x] PyPI publication (v0.2.0)
- [ ] Comprehensive unit tests
- [ ] Sphinx documentation + ReadTheDocs
- [ ] Hero 11/12/13 support

### Q2 2026: GyroFlow Integration 🎯
- [ ] Export gyro data for GyroFlow
- [ ] Video stabilization workflow
- [ ] Python API integration

### Q3 2026: ML Analytics 🤖
- [ ] Automatic activity detection
- [ ] Trip analysis & statistics
- [ ] Interactive dashboards (Plotly)

### Q4 2026: Real-time & Streaming 📡
- [ ] Live telemetry streaming
- [ ] WebSocket API
- [ ] OBS Studio integration

📖 **Full roadmap**: [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Help needed with**:
- Testing with Hero 11/12/13 files
- Documentation & examples
- Feature development
- Bug reports & feedback

---

## 📚 Documentation

- **Quick Start**: [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
- **Full Roadmap**: [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md)
- **Russian Documentation**: [README_RU.md](README_RU.md)
- **Windows Installation**: [WINDOWS_INSTALL.md](WINDOWS_INSTALL.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

## 🔗 Related Projects

- [GoPro GPMF Parser](https://github.com/gopro/gpmf-parser) - Official C/C++ parser
- [GyroFlow](https://github.com/gyroflow/gyroflow) - Video stabilization using gyro data
- [Telemetry Extractor](https://goprotelemetryextractor.com/) - Commercial GUI tool

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits & Attribution

**Author & Maintainer**: ozand  
**Original Project**: [pygpmf](https://github.com/alexis-mignon/pygpmf) by Alexis Mignon

This project (`pygpmf-oz`) is a modernized fork of the original `pygpmf` library by Alexis Mignon.  
Key improvements include Python 3.9-3.13 support, Windows compatibility, and active maintenance.

**Contributors**: See [CHANGELOG.md](CHANGELOG.md)

---

**⭐ If you find this useful, please star the repo!**  
**📦 PyPI**: https://pypi.org/project/pygpmf-oz/  
**🐛 Issues**: https://github.com/ozand/pygpmf-oz/issues


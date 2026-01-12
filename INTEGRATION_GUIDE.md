# pygpmf_oz v0.3.0 Integration Guide

For teams upgrading from **pygpmf-oz 0.2.1** and implementing GoPro telemetry extraction.

---

## What's New in 0.3.0

### ✅ Hero 11-13 GPS9 Support (10Hz)
- **GPS5 (Hero 5-10)**: 5-field structure, 5Hz sampling  
- **GPS9 (Hero 11-13)**: 9-field structure, 10Hz sampling, includes Dilution of Precision (DOP) and fix status  
- **Auto-detection**: Library automatically selects GPS5 or GPS9 based on stream presence  
- **Backward compatible**: GPS5 extraction unaffected; GPS9 extracts first 5 fields for GPSData compatibility

### 🛰️ Gyroscope & Accelerometer (IMU)
- **New module**: `gpmf.gyro` with `GyroData` and `AccelData` containers  
- **3-axis support**: X, Y, Z angular velocity (rad/s) and linear acceleration (m/s²)  
- **Foundation for GyroFlow**: Exports placeholder functions for v0.3.1+ stabilization  

### 🐛 UTF-8 FourCC Decode Fix
- **Issue in 0.2.1**: UnicodeDecodeError on binary FourCC codes  
- **Fix in 0.3.0**: ASCII/latin-1 decoding with error handling  
- **Impact**: No more crashes on non-ASCII GoPro GPMF metadata

---

## Installation

### Upgrade from 0.2.1
```bash
pip install --upgrade pygpmf-oz
```

### Fresh Install
```bash
pip install pygpmf-oz>=0.3.0
```

### System Requirements
- **FFmpeg** required (for GPMF stream extraction)
  - **Windows**: `choco install ffmpeg` or `scoop install ffmpeg`
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `apt-get install ffmpeg` (Ubuntu/Debian)

---

## Integration Pattern: FFmpeg-First Extraction (Critical)

⚠️ **Important**: Do NOT pass raw MP4 file bytes directly to `gpmf.parse.iter_klv()`. The GPMF stream is embedded in the MP4 container and must be extracted first.

### Correct Approach

```python
import subprocess
from pygpmf import parse, gps

video_path = "S:/GoPro/video.mp4"

# Step 1: Extract GPMF stream using FFmpeg
cmd = [
    'ffmpeg',
    '-i', video_path,
    '-c', 'copy',
    '-map', '0:3',        # GPMF stream is usually index 3
    '-f', 'rawvideo',
    '-'
]
result = subprocess.run(cmd, capture_output=True, timeout=30)
gpmf_data = result.stdout

# Step 2: Parse with pygpmf-oz
gps_blocks = list(gps.extract_gps_blocks(gpmf_data))

# Step 3: Process GPS blocks
for block in gps_blocks:
    gps_data = gps.parse_gps_block(block)
    print(f"Lat: {gps_data.latitude}, Lon: {gps_data.longitude}")
```

### Why FFmpeg-First?
- Raw MP4 contains many binary structures; FourCC codes can be garbage when not properly demuxed
- FFmpeg extracts the clean GPMF stream from the `gpmd` atom
- Prevents false positives and decoding errors

---

## GPS Data Interpretation

### Fix Status Values
The `fix` field in `GPSData` indicates satellite lock:

| Value | Meaning | Coordinates                   |
| ----- | ------- | ----------------------------- |
| `0`   | No fix  | All zeros                     |
| `2`   | 2D fix  | Valid lat/lon, alt unreliable |
| `3`   | 3D fix  | Valid lat/lon/alt             |

### "No Fix" Scenario
When `fix == 0`:
- Video was recorded without GPS signal lock
- Latitude/longitude/altitude all read as 0.0
- This is **not** a parsing error; it reflects the camera's state
- Common with indoor or cloudy-day recording

**Recommended handling:**
```python
if gps_data.fix == 0:
    print(f"No GPS signal during recording (fix={gps_data.fix})")
    continue  # Skip this block
elif gps_data.fix in [2, 3]:
    # Valid GPS data
    process_coordinates(gps_data)
```

---

## Hero 11-13 Specific Notes

### GPS9 Field Breakdown
When parsing GPS9, all 9 fields are available, but only the first 5 are used for GPSData compatibility:

| Field # | Name                        | Unit | Used? |
| ------- | --------------------------- | ---- | ----- |
| 1       | Latitude                    | deg  | ✅     |
| 2       | Longitude                   | deg  | ✅     |
| 3       | Altitude                    | m    | ✅     |
| 4       | Speed (2D)                  | m/s  | ✅     |
| 5       | Speed (3D)                  | m/s  | ✅     |
| 6       | Days since 2000             | days | —     |
| 7       | Seconds since midnight      | s    | —     |
| 8       | DOP (Dilution of Precision) | —    | —     |
| 9       | Fix status                  | —    | —     |

Future versions will expose fields 6-9 for advanced analytics.

### Detecting Camera Model
Use `MINF` field for camera identification:
```python
from pygpmf import parse

with open(video_path, 'rb') as f:
    data = f.read()

# Extract MINF stream
minf_blocks = list(parse.filter_klv(data, 'MINF'))
if minf_blocks:
    model_info = minf_blocks[0].value
    print(f"Camera: {model_info}")  # e.g., "GoPro Hero 13"
```

---

## Troubleshooting

### Error: `No GPS data found`
**Causes:**
1. Video recorded without GPS signal → Check `gps_data.fix` value
2. Not using FFmpeg extraction → Use the pattern above
3. Wrong FFmpeg stream index → Try `-map 0:1`, `-map 0:2`, etc.

**Solution:**
```bash
# Find GPMF stream
ffmpeg -i video.mp4 2>&1 | grep -i stream
# Look for "gpmd" atom

# Try different indices
for i in 0 1 2 3 4 5; do
  ffmpeg -i video.mp4 -map 0:$i -f rawvideo - 2>/dev/null | xxd | head -20
done
```

### Error: `UnicodeDecodeError` (0.2.1 only)
**Upgrade to 0.3.0:**
```bash
pip install --upgrade pygpmf-oz==0.3.0
```

No patch needed in 0.3.0+.

---

## Gyroscope/Accelerometer Extraction

New in 0.3.0:

```python
from pygpmf import gyro

# After FFmpeg extraction (see pattern above)
gyro_blocks = list(gyro.extract_gyro_blocks(gpmf_data))
accel_blocks = list(gyro.extract_accel_blocks(gpmf_data))

for block in gyro_blocks:
    gyro_data = gyro.parse_gyro_block(block)
    print(f"X: {gyro_data.x} rad/s")  # Angular velocity
    print(f"Y: {gyro_data.y} rad/s")
    print(f"Z: {gyro_data.z} rad/s")

for block in accel_blocks:
    accel_data = gyro.parse_accel_block(block)
    print(f"X: {accel_data.x} m/s²")  # Linear acceleration
    print(f"Y: {accel_data.y} m/s²")
    print(f"Z: {accel_data.z} m/s²")
```

**Future versions (v0.3.1+):**
- GyroFlow JSON export for video stabilization
- IMU integration for rotation calculation

---

## Comparing 0.2.1 vs 0.3.0

| Feature           | 0.2.1  | 0.3.0           |
| ----------------- | ------ | --------------- |
| GPS5 support      | ✅      | ✅               |
| GPS9 (Hero 11-13) | ❌      | ✅               |
| Gyroscope/Accel   | ❌      | ✅ (read-only)   |
| UTF-8 FourCC fix  | ❌      | ✅               |
| GyroFlow export   | ❌      | 🔄 (placeholder) |
| Test coverage     | 83.67% | 79.77%          |
| Total tests       | 119    | 134             |

---

## FAQ

**Q: Do I need to use FFmpeg extraction for all videos?**  
A: Yes, it's the reliable way to get the GPMF stream. Direct MP4 parsing may work for some files but fails on others.

**Q: My Hero 11 video has GPS9 but `gps.extract_gps_blocks()` finds nothing?**  
A: Confirm GPMF stream was extracted with FFmpeg and has non-zero size. Use `ffmpeg -i video.mp4 2>&1` to verify the `gpmd` atom exists.

**Q: Can I extract gyro and accel simultaneously with GPS?**  
A: Yes! All three streams are independent and can be extracted from the same `gpmf_data`:
```python
gps_blocks = list(gps.extract_gps_blocks(gpmf_data))
gyro_blocks = list(gyro.extract_gyro_blocks(gpmf_data))
accel_blocks = list(gyro.extract_accel_blocks(gpmf_data))
```

**Q: When will GyroFlow stabilization export be available?**  
A: Planned for v0.3.1 (Q1 2026). Currently module has placeholder functions.

---

## References

- **pygpmf-oz on PyPI**: https://pypi.org/project/pygpmf-oz/
- **GitHub Repository**: https://github.com/ozand/pygpmf_oz
- **GPMF Spec**: https://github.com/gopro/gpmf-parser
- **GyroFlow Project**: https://github.com/gyroflow/gyroflow

---

**Need help?** Open an issue on GitHub: https://github.com/ozand/pygpmf_oz/issues

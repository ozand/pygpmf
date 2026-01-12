# pygpmf_oz v0.3.0 Release Summary

**Release Date**: January 12, 2026  
**Status**: ✅ Ready for PyPI Publication

---

## Executive Summary

Released **pygpmf_oz v0.3.0** with:
- ✅ **Hero 11-13 GPS9 support** (10Hz, 9-field structure)
- ✅ **Gyroscope/Accelerometer module** for IMU telemetry
- ✅ **UTF-8 FourCC decode fix** (resolves 0.2.1 crashes)
- ✅ **134 comprehensive tests** (79.77% coverage)
- ✅ **Full backward compatibility** with Hero 5-10 (GPS5)

---

## Build Artifacts

| Artifact                           | Size    | Status     |
| ---------------------------------- | ------- | ---------- |
| `pygpmf_oz-0.3.0-py3-none-any.whl` | 33.8 KB | ✅ Verified |
| `pygpmf_oz-0.3.0.tar.gz`           | 30.4 KB | ✅ Verified |

Both pass `twine check` with no warnings.

---

## Test Results

```
============================= 134 passed in 3.92s =============================

Coverage Summary:
  gpmf/__init__.py      100.00%
  gpmf/__main__.py       91.95%
  gpmf/gps.py            83.33%  (+16.66% from GPS9 tests)
  gpmf/gyro.py           48.00%  (new module)
  gpmf/io.py             87.50%
  gpmf/parse.py          90.91%
  gpmf/gps_plot.py       67.21%
  ────────────────────────────────
  TOTAL                  79.77%
```

**Improvement from 0.2.1**: 119 tests → 134 tests (+15 new tests for GPS9 & gyro)

---

## New Features by Category

### 🛰️ GPS Data (Task 5 Phase 1)
- **GPS9 Auto-Detection**: Library automatically chooses GPS5 or GPS9 based on stream presence
- **Hero 11-13 Support**: Parses 9-field GPS9 structure with proper scaling
- **Backward Compatible**: GPS5 path unchanged; GPS9 extracts first 5 fields for compatibility
- **Tests**: 7 new GPS9-specific tests in `test_hero11_support.py`
- **Coverage**: `gps.py` improved from 66.67% → 83.33%

### 📡 Gyroscope & Accelerometer (Task 5 Phase 2)
- **New Module**: `gpmf.gyro` with `GyroData` and `AccelData` namedtuples
- **Data Extraction**: `parse_gyro_block()`, `parse_accel_block()` functions
- **Stream Generators**: `extract_gyro_blocks()`, `extract_accel_blocks()`
- **GyroFlow Foundation**: Placeholder functions for v0.3.1+ stabilization export
- **Tests**: 8 new IMU tests in `test_gyro.py`
- **Coverage**: New module at 48% (ready for expansion)

### 🐛 Bug Fixes
- **UTF-8 FourCC Decode**: Fixed UnicodeDecodeError by using ASCII/latin-1 decoding with error handling
- **No Impact on 0.2.1 Users**: Library gracefully handles edge cases now

---

## Documentation Additions

| Document                           | Purpose                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------ |
| `INTEGRATION_GUIDE.md`             | FFmpeg-first extraction pattern, GPS fix interpretation, troubleshooting |
| `HERO11_SUPPORT.md`                | Technical specs: GPS9 fields, binary formats, compatibility matrix       |
| `examples/example_gps9_extract.py` | GPS9 extraction and GPX export demo                                      |
| `examples/example_gyro_extract.py` | Gyro/accel data parsing example                                          |

---

## Upgrade Path: 0.2.1 → 0.3.0

### Installation
```bash
pip install --upgrade pygpmf-oz
```

### What External Teams Need to Know

1. **FFmpeg-First Extraction** (Critical)
   - Do NOT parse raw MP4 bytes directly
   - Use FFmpeg to extract GPMF stream first (`-map 0:3`)
   - See `INTEGRATION_GUIDE.md` for full pattern

2. **GPS "No Fix" Handling**
   - Videos without satellite lock: `fix=0`, coordinates all zeros
   - Not a parsing error; reflects camera state
   - Recommend filtering: `if gps_data.fix in [2, 3]: process()`

3. **Breaking Changes**: NONE
   - GPS5 API unchanged
   - All existing code works as-is
   - GPS9 transparently used when available

### Benefits of Upgrading
- ✅ No more UnicodeDecodeError on certain GoPro models
- ✅ Support for Hero 11-13 recordings with GPS9
- ✅ New gyroscope/accelerometer data for analytics
- ✅ Better error messages and handling

---

## Commits in This Release

```
04113b7 Add comprehensive integration guide for external teams upgrading to v0.3.0
b0bd22c Update documentation: finalize Task 5 reports and Hero 11-13 specs
7ff39a3 Release 0.3.0: Hero 11-13 telemetry support
9af91e2 Add Hero 11-13 GPS9 and gyroscope example scripts
705eaea Add Task 5 Hero 11-13 Support completion report
1840981 Export gyro module in package __init__.py
d2fab65 Add gyroscope and accelerometer module for GyroFlow integration
d1c52f1 Implement Hero 11-13 GPS9 support with comprehensive tests
```

---

## Next Steps (v0.3.1+)

- **GyroFlow Integration**: Export IMU data in GyroFlow JSON format for video stabilization
- **IMU Rotation Calculation**: Integrate gyro data to compute camera rotation angles
- **Analytics Module**: Activity detection, trip metrics, elevation profiles
- **MINF Field Parsing**: Extract camera model info from telemetry

---

## PyPI Information

**Package**: [pygpmf-oz](https://pypi.org/project/pygpmf-oz/)  
**Latest Release**: 0.3.0 (pending)  
**Python Support**: 3.9, 3.10, 3.11, 3.12, 3.13  
**Platforms**: Windows, macOS, Linux  
**License**: MIT

---

## Contact & Support

- **GitHub**: https://github.com/ozand/pygpmf_oz
- **Issues**: https://github.com/ozand/pygpmf_oz/issues
- **PyPI**: https://pypi.org/project/pygpmf-oz/

---

**Ready for publication to PyPI!** Use `PYPI_UPLOAD_0_3_0.md` for upload instructions.

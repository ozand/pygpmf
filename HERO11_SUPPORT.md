# Hero 11-13 Support: Technical Implementation Plan

## Implementation Status

### Phase 1: Research ✅ (Complete)
- GPMF format analysis completed
- GPS evolution documented (Hero 5-13)
- GPS9 structure specifications identified
- Binary format and scaling factors determined
- Compatibility matrix created

### Phase 2: GPS9 Parsing ✅ (Complete - Commit d1c52f1)
- Updated `extract_gps_blocks()` to detect both GPS5 and GPS9 streams
- Modified `parse_gps_block()` to handle GPS9's 9-field structure
- Implemented backward compatibility with GPS5 (extracts first 5 fields)
- Added 7 comprehensive Hero 11-13 tests in `tests/test_hero11_support.py`
- Coverage improved: 82% → 85% (126 total tests)
- Test results: All 126 tests passing ✅

### Phase 3: Advanced Features (Pending)
- MINF field parsing (camera model detection)
- Gyroscope data (GYRO) parsing for stabilization
- Accelerometer data (ACCL) parsing
- Integration with GyroFlow JSON export

## Research Complete ✅

Comprehensive GPMF format analysis completed with detailed specifications for Hero 5-13 evolution.

## Key Findings

### GPS Evolution
- **Hero 5-10**: GPS5 at 5Hz
- **Hero 11-13**: GPS5 at 10Hz (deprecated) + GPS9 at 10Hz (new)
- **Hero 12**: NO GPS (battery savings)
- **Hero 13**: GPS9 at 10Hz (restored)

### New GPMF Fields (Hero 11+)
| Field | Type            | Frequency | Purpose                            |
| ----- | --------------- | --------- | ---------------------------------- |
| GPS9  | Complex 9-field | 10Hz      | Enhanced GPS with DOP & fix status |
| GPSU  | UTC string      | 1Hz       | Precise time with milliseconds     |
| GPSF  | Byte            | 1Hz       | Fix status (0/2/3)                 |
| GPSP  | Short           | 1Hz       | Dilution of Precision              |
| GPSA  | Reference       | 1Hz       | Altitude system (WGS84)            |
| MINF  | Model ID        | Once      | Camera model identification        |

### GPS9 Structure (Hero 11+)
```
GPS9: latitude, longitude, altitude, speed_2d, speed_3d, 
      days_since_2000, seconds_since_midnight, dop, fix_status
```

### Compatibility Matrix
| Feature        | Hero 5-10 | Hero 11      | Hero 12 | Hero 13      |
| -------------- | --------- | ------------ | ------- | ------------ |
| GPS5           | 5Hz       | 10Hz         | None    | None         |
| GPS9           | -         | ✓            | -       | ✓            |
| Time precision | Low       | ms precision | -       | ms precision |

## Implementation Strategy

### Phase 1: Detection & Compatibility
- [ ] Detect camera model from MINF field
- [ ] Detect GPS frequency (5Hz vs 10Hz)
- [ ] Handle Hero 12 (no GPS case)
- [ ] Backward compatibility with Hero 5-10

### Phase 2: GPS9 Parsing
- [ ] Implement GPS9 complex structure parser
- [ ] Handle scaling factors properly
- [ ] Extract millisecond-precision timestamps
- [ ] Parse DOP and fix status

### Phase 3: Testing
- [ ] Unit tests for GPS9 parsing
- [ ] Hero 11 sample data validation
- [ ] Hero 12 skip logic
- [ ] Hero 13 compatibility check

### Phase 4: Integration
- [ ] Update gps.py extract_gps() for Hero 11+
- [ ] Add camera detection to parse.py
- [ ] Update documentation
- [ ] Create examples for Hero 11-13

## Testing Data Sources

**Official Resources**:
- GoPro GPMF Parser: https://github.com/gopro/gpmf-parser
- Sample videos: GoPro GPMF test suite
- Hero 11 specifications: Official GoPro docs

**Community Resources**:
- gopro-telemetry: JavaScript reference implementation
- Trek View GPMF analysis
- GoPro Telemetry Extractor

## References

- Official GPMF parser: https://gopro.github.io/gpmf-parser/
- Binary format spec: KLV with 32-bit alignment
- U-Blox MAX-M10S datasheet (Hero 11/13 receiver)
- Hero 12 specifications (no GPS module)

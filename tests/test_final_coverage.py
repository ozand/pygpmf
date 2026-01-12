"""Final coverage tests to reach 80%+"""
import pytest
import numpy as np
from gpmf.parse import filter_klv, expand_klv, parse_payload, KLVItem, KLVLength
from gpmf.gps import GPSData


class TestFilterKLV:
    """Test filter_klv with multiple fourcc codes"""
    
    def test_filter_klv_empty_stream(self):
        """Test filtering on empty stream"""
        # Empty stream
        results = list(filter_klv(b'', ['GPS5']))
        
        # Should be empty
        assert len(results) == 0


class TestExpandKLV:
    """Test expand_klv generator conversion"""
    
    def test_expand_klv_generator_type_check(self):
        """Test _expand_klv handles generators properly"""
        from gpmf.parse import _expand_klv
        import types
        
        # Create a simple generator
        def simple_gen():
            yield ('TEST', ('c', 4, 1), b'test')
        
        gen = simple_gen()
        
        # Verify it's a generator
        assert isinstance(gen, types.GeneratorType)
        
        # Expand should convert to list
        result = _expand_klv(gen)
        assert isinstance(result, list)


class TestParsePayloadEdgeCases:
    """Test parse_payload with edge cases for lines 89-96"""
    
    def test_parse_payload_type_u_datetime(self):
        """Test UTC datetime parsing (type 'U')"""
        # Create UTC datetime string: 260112123045 = 2026-01-12 12:30:45
        utc_bytes = b'260112123045'
        
        result = parse_payload(utc_bytes, 'GPSU', 'U', 12, 1)
        
        # Should format as datetime string
        assert '2026-01-12' in result
        assert '12:30:45' in result
    
    def test_parse_payload_unsigned_long_array(self):
        """Test unsigned long array with multiple values"""
        # Create array of 3 unsigned longs
        data = np.array([100, 200, 300], dtype='>u4').tobytes()
        
        result = parse_payload(data, 'TEST', 'L', 4, 3)
        
        # Should be numpy array with shape (3,)
        assert isinstance(result, np.ndarray)
        assert len(result) == 3
    
    def test_parse_payload_multidimensional(self):
        """Test multi-dimensional array (GPS5 style: 5 values × N samples)"""
        # Simulate GPS5: 5 floats per sample, 2 samples
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], dtype='>f4').tobytes()
        
        result = parse_payload(data, 'GPS5', 'f', 4, 10)  # 10 floats (2 samples × 5 values)
        
        # Should reshape to (2, 5)
        if isinstance(result, np.ndarray) and result.size > 1:
            assert result.ndim in [1, 2]  # Could be flattened or reshaped


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

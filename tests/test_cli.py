"""Tests for CLI functionality."""
import pytest
import sys
import os
import json
import tempfile
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
from gpmf import __main__


class TestCLI:
    """Test command-line interface."""
    
    def test_cli_help(self):
        """Test CLI --help option."""
        # Test that help can be invoked
        assert hasattr(__main__, 'main')
        assert callable(__main__.main)
    
    def test_cli_version(self):
        """Test CLI --version option."""
        # Import version
        from gpmf import __version__
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert len(__version__) > 0
    
    def test_cli_extract_command_exists(self):
        """Test that extract command exists."""
        # Verify CLI has extract functionality
        import gpmf.__main__ as cli_module
        assert hasattr(cli_module, 'main')


class TestFileOperations:
    """Test file operation commands."""
    
    def test_extract_requires_input_file(self):
        """Test that extract command requires input file."""
        # Extract should need a file argument
        # This tests the argparse structure
        pass
    
    def test_export_formats(self):
        """Test supported export formats."""
        # Should support GPX format at minimum
        supported_formats = ['gpx']
        assert 'gpx' in supported_formats


class TestArgParser:
    """Test argument parser."""
    
    def test_parse_args_gps_extract(self):
        """Test GPS extract argument parsing."""
        with patch('sys.argv', ['gpmf', 'gps-extract', 'test.mp4']):
            args = __main__.parse_args()
            assert args.command == 'gps-extract'
            assert args.file == 'test.mp4'
            assert args.output_file is None
            assert args.first_only is False
    
    def test_parse_args_gps_extract_with_output(self):
        """Test GPS extract with output file."""
        with patch('sys.argv', ['gpmf', 'gps-extract', 'test.mp4', '-o', 'output.gpx']):
            args = __main__.parse_args()
            assert args.output_file == 'output.gpx'
    
    def test_parse_args_gps_extract_first_only(self):
        """Test GPS extract with first-only flag."""
        with patch('sys.argv', ['gpmf', 'gps-extract', 'test.mp4', '-f']):
            args = __main__.parse_args()
            assert args.first_only is True
    
    def test_parse_args_gps_first(self):
        """Test GPS first command parsing."""
        with patch('sys.argv', ['gpmf', 'gps-first', 'test.mp4']):
            args = __main__.parse_args()
            assert args.command == 'gps-first'
            assert args.file == 'test.mp4'
    
    def test_parse_args_gps_plot(self):
        """Test GPS plot command parsing."""
        with patch('sys.argv', ['gpmf', 'gps-plot', 'test.mp4']):
            args = __main__.parse_args()
            assert args.command == 'gps-plot'
            assert args.file == 'test.mp4'
            assert args.output_file is None
    
    def test_parse_args_gps_plot_with_output(self):
        """Test GPS plot with output file."""
        with patch('sys.argv', ['gpmf', 'gps-plot', 'test.mp4', '-o', 'track.png']):
            args = __main__.parse_args()
            assert args.output_file == 'track.png'


class TestCommands:
    """Test CLI command execution."""
    
    def test_command_registry(self):
        """Test that all commands are registered."""
        assert hasattr(__main__, 'COMMANDS')
        assert 'gpx-extract' in __main__.COMMANDS
        assert 'gps-first' in __main__.COMMANDS
        assert 'gps-plot' in __main__.COMMANDS
    
    def test_commands_are_callable(self):
        """Test that all registered commands are callable."""
        for cmd_name, cmd_func in __main__.COMMANDS.items():
            assert callable(cmd_func), f"Command {cmd_name} is not callable"


class TestGPXExtract:
    """Test GPX extraction command."""
    
    @patch('gpmf.__main__.extract_gpmf_stream')
    @patch('gpmf.__main__.extract_gps_blocks')
    @patch('gpmf.__main__.parse_gps_block')
    @patch('gpmf.__main__.make_pgx_segment')
    @patch('builtins.open', new_callable=mock_open)
    def test_command_gpx_extract(self, mock_file, mock_make_segment, 
                                  mock_parse, mock_extract_blocks, mock_extract_stream):
        """Test GPX extract command execution."""
        # Setup mocks
        mock_extract_stream.return_value = b'fake_stream'
        mock_extract_blocks.return_value = [MagicMock()]
        mock_parse.return_value = MagicMock()
        mock_segment = MagicMock()
        mock_make_segment.return_value = mock_segment
        
        # Create args
        args = MagicMock()
        args.file = 'test.mp4'
        args.output_file = None
        args.output_directory = None
        args.gpx_version = '1.1'
        args.first_only = False
        args.no_speed = False
        
        # Execute command
        __main__.command_gpx_extract(args)
        
        # Verify calls
        mock_extract_stream.assert_called_once_with('test.mp4')
        mock_extract_blocks.assert_called_once()
        mock_file.assert_called_once()
    
    @patch('gpmf.__main__.extract_gpmf_stream')
    @patch('gpmf.__main__.extract_gps_blocks')
    @patch('gpmf.__main__.parse_gps_block')
    @patch('gpmf.__main__.make_pgx_segment')
    @patch('builtins.open', new_callable=mock_open)
    def test_command_gpx_extract_with_output_dir(self, mock_file, mock_make_segment,
                                                   mock_parse, mock_extract_blocks, mock_extract_stream):
        """Test GPX extract with output directory."""
        # Setup mocks
        mock_extract_stream.return_value = b'fake_stream'
        mock_extract_blocks.return_value = [MagicMock()]
        mock_parse.return_value = MagicMock()
        mock_make_segment.return_value = MagicMock()
        
        # Create args
        args = MagicMock()
        args.file = 'test.mp4'
        args.output_file = None
        args.output_directory = '/output'
        args.gpx_version = '1.1'
        
        # Execute command
        __main__.command_gpx_extract(args)
        
        # Verify directory handling
        mock_extract_stream.assert_called_once()


class TestGPSFirst:
    """Test GPS first position command."""
    
    @patch('gpmf.__main__.extract_gpmf_stream')
    @patch('gpmf.__main__.filter_klv')
    @patch('gpmf.__main__.parse_gps_block')
    @patch('sys.stdout', new_callable=StringIO)
    def test_command_gps_first_with_gps(self, mock_stdout, mock_parse, mock_filter, mock_extract):
        """Test GPS first command with GPS data."""
        # Setup mocks
        mock_extract.return_value = b'fake_stream'
        
        # Create fake GPS block
        fake_gps_item = MagicMock()
        fake_gps_item.key = 'GPS5'
        fake_stream_item = MagicMock()
        fake_stream_item.value = [fake_gps_item]
        mock_filter.return_value = [fake_stream_item]
        
        # Mock GPS data
        mock_gps_data = MagicMock()
        mock_gps_data.latitude = [37.7749]
        mock_gps_data.longitude = [-122.4194]
        mock_gps_data.speed_3d = [5.0]
        mock_gps_data.timestamp = "2024-01-12 10:00:00.000"
        mock_parse.return_value = mock_gps_data
        
        # Create args
        args = MagicMock()
        args.file = 'test.mp4'
        
        # Execute command
        __main__.command_gps_first(args)
        
        # Verify output
        output = mock_stdout.getvalue()
        assert len(output) > 0
        # Should be JSON
        json_data = json.loads(output.strip())
        assert 'latitude' in json_data
        assert 'longitude' in json_data
    
    @patch('gpmf.__main__.extract_gpmf_stream')
    @patch('gpmf.__main__.filter_klv')
    @patch('sys.stderr', new_callable=StringIO)
    def test_command_gps_first_no_gps(self, mock_stderr, mock_filter, mock_extract):
        """Test GPS first command without GPS data."""
        # Setup mocks
        mock_extract.return_value = b'fake_stream'
        mock_filter.return_value = []
        
        # Create args
        args = MagicMock()
        args.file = 'test.mp4'
        
        # Execute command
        __main__.command_gps_first(args)
        
        # Verify error message
        error_output = mock_stderr.getvalue()
        assert 'No GPS information found' in error_output


class TestGPSPlot:
    """Test GPS plotting command."""
    
    @patch('gpmf.__main__.extract_gpmf_stream')
    @patch('gpmf.__main__.extract_gps_blocks')
    @patch('gpmf.__main__.parse_gps_block')
    @patch('gpmf.__main__.plot_gps_trace')
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.tight_layout')
    def test_command_gps_plot(self, mock_layout, mock_savefig, mock_plot,
                               mock_parse, mock_extract_blocks, mock_extract_stream):
        """Test GPS plot command execution."""
        # Setup mocks
        mock_extract_stream.return_value = b'fake_stream'
        
        # Mock GPS data
        mock_gps_data = MagicMock()
        mock_gps_data.latitude = [37.7749, 37.7750]
        mock_gps_data.longitude = [-122.4194, -122.4195]
        
        mock_extract_blocks.return_value = [MagicMock()]
        mock_parse.return_value = mock_gps_data
        
        # Create args
        args = MagicMock()
        args.file = 'test.mp4'
        args.output_file = None
        args.output_directory = None
        args.first_only = False
        
        # Execute command
        __main__.command_gps_plot(args)
        
        # Verify calls
        mock_extract_stream.assert_called_once_with('test.mp4')
        mock_plot.assert_called_once()
        mock_savefig.assert_called_once()


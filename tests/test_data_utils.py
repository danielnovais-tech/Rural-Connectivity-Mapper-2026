"""Tests for data utilities."""

import pytest
import json
from pathlib import Path

from src.utils.data_utils import load_data, save_data, backup_data


@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return [
        {
            'id': 'test-1',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'provider': 'Starlink'
        },
        {
            'id': 'test-2',
            'latitude': -22.9068,
            'longitude': -43.1729,
            'provider': 'Claro'
        }
    ]


def test_load_save_data(tmp_path, sample_data):
    """Test saving and loading JSON data."""
    test_file = tmp_path / "test_data.json"
    
    # Save data
    save_data(str(test_file), sample_data)
    
    assert test_file.exists()
    
    # Load data
    loaded_data = load_data(str(test_file))
    
    assert len(loaded_data) == 2
    assert loaded_data[0]['id'] == 'test-1'
    assert loaded_data[1]['provider'] == 'Claro'


def test_backup_data(tmp_path, sample_data):
    """Test creating backup of data file."""
    test_file = tmp_path / "test_data.json"
    
    # Create original file
    save_data(str(test_file), sample_data)
    
    # Create backup
    backup_path = backup_data(str(test_file))
    
    assert Path(backup_path).exists()
    assert 'backup' in backup_path
    
    # Verify backup content matches original
    original_data = load_data(str(test_file))
    backup_data_content = load_data(backup_path)
    
    assert original_data == backup_data_content


def test_load_nonexistent_file(tmp_path):
    """Test loading from non-existent file."""
    test_file = tmp_path / "nonexistent.json"
    
    # Should return empty list without error
    data = load_data(str(test_file))
    
    assert data == []


def test_backup_nonexistent_file(tmp_path):
    """Test backup of non-existent file raises error."""
    test_file = tmp_path / "nonexistent.json"
    
    with pytest.raises(FileNotFoundError):
        backup_data(str(test_file))


def test_save_creates_directory(tmp_path, sample_data):
    """Test that save_data creates parent directories."""
    test_file = tmp_path / "subdir" / "nested" / "test_data.json"
    
    # Should create directories automatically
    save_data(str(test_file), sample_data)
    
    assert test_file.exists()
    
    # Verify data
    loaded_data = load_data(str(test_file))
    assert len(loaded_data) == 2

import pytest
import numpy as np

@pytest.fixture
def white_frame():
    """A 1080p white frame (255)"""
    return np.full((1080, 1920, 3), 255, dtype=np.uint8)

@pytest.fixture
def black_frame():
    """A 1080p black frame (0)"""
    return np.zeros((1080, 1920, 3), dtype=np.uint8)

@pytest.fixture
def mid_gray_frame():
    """A 1080p mid-gray frame (128)"""
    return np.full((1080, 1920, 3), 128, dtype=np.uint8)

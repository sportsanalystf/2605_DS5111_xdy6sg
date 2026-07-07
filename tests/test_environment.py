"""
test_environment.py - Environment and pipeline validation tests.
Covers: OS check, Python version, xfail, skipif, and parametrized cases.
"""

import sys
import platform
import re
import pytest


def is_valid_youtube_id(video_id):
    """Return True if video_id matches YouTube's 11-char Base64url format."""
    pattern = re.compile(r'^[A-Za-z0-9_\-]{11}$')
    return bool(pattern.match(video_id))


def test_running_on_linux():
    """Pipeline should run on Linux/Ubuntu."""
    assert platform.system() == "Linux", (
        f"Expected Linux, got: {platform.system()}"
    )


def test_python_version_is_supported():
    """Verify the runtime Python version is 3.8 or newer."""
    major, minor = sys.version_info.major, sys.version_info.minor
    assert (major, minor) >= (3, 8), (
        f"Python 3.8+ required, running {major}.{minor}"
    )


@pytest.mark.xfail(reason="Deduplication not yet implemented in pipeline")
def test_duplicate_ids_are_deduplicated():
    """Expected to fail until dedup logic is added."""
    input_ids = ["abc123abc12", "abc123abc12", "xyz789xyz78"]
    unique_ids = list(set(input_ids))
    assert len(unique_ids) == 3


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows-specific path test, skipped on Linux"
)
def test_windows_path_separator():
    """Skipped on Linux — only relevant on Windows environments."""
    path = "C:\\Users\\test"
    assert "\\" in path

@pytest.mark.parametrize("video_id,expected", [
    ("CctJNYYCPo0", True),
    ("dQw4w9WgXcQ", True),
    ("abcd", False),
    ("1234", False),
    ("123456789012", False),
    ("invalid id!", False),
    ("", False),
])
def test_youtube_id_validation(video_id, expected):
    """Parametrized: validate various IDs against the 11-char Base64url rule."""
    assert is_valid_youtube_id(video_id) == expected

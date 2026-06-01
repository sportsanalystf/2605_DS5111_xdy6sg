import sys
import io
import platform
import pytest
from bin.clean_ids import main


# --- Script tests ---

def test_valid_id_passes(monkeypatch, capsys):
    """A single valid ID should be echoed to stdout."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("kcFsuxaJ1es\n"))
    main()
    captured = capsys.readouterr()
    assert captured.out == "kcFsuxaJ1es\n"


def test_invalid_id_suppressed(monkeypatch, capsys):
    """An invalid ID should produce no stdout output."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("asd123\n"))
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_valid_and_invalid_mixed(monkeypatch, capsys):
    """Valid IDs pass, invalid ones are suppressed."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("kcFsuxaJ1es\nasd123\nCctJNYYCPo0\n"))
    main()
    captured = capsys.readouterr()
    assert captured.out == "kcFsuxaJ1es\nCctJNYYCPo0\n"


def test_10_char_id_invalid(monkeypatch, capsys):
    """10 character ID should be rejected (too short)."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("kcFsuxaJ1e\n"))
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_12_char_id_invalid(monkeypatch, capsys):
    """12 character ID should be rejected (too long)."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("kcFsuxaJ1es1\n"))
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_only_bad_lines(monkeypatch, capsys):
    """All invalid lines should produce no stdout output."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("abcd\n1234\n"))
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


# --- Environment tests ---

def test_running_on_linux():
    """Should be running on Linux."""
    assert platform.system() == "Linux"


def test_running_on_ubuntu():
    """Should be running on Ubuntu."""
    with open("/etc/os-release") as f:
        contents = f.read()
    assert "Ubuntu" in contents


def test_python_version():
    """Should be running Python 3.14."""
    assert sys.version_info.major == 3
    assert sys.version_info.minor == 14


@pytest.mark.xfail
def test_expected_to_fail():
    """Placeholder: expected to fail."""
    assert 1 == 2


@pytest.mark.skip(reason="feature not yet implemented")
def test_skipped():
    """Placeholder: skipped until feature is ready."""
    assert False

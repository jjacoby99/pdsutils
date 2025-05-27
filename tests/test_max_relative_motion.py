import pytest
from pdsutils import maximum_relative_rotation

def test_dummy(tmp_path, monkeypatch):
    # you can mock out file reads or just assert that
    # calling it with no files raises a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        maximum_relative_rotation(str(tmp_path), [1], [1], ["walkway1"], ts=0.0)


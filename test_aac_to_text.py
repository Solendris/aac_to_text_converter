from unittest.mock import patch, MagicMock
import sys
sys.modules['whisper'] = MagicMock()
import aac_to_text


def test_save_to_file_success(tmp_path):
    output = tmp_path / "test.txt"
    aac_to_text.save_to_file("test", output)
    assert output.exists() is True
    assert output.read_text() == "test"

def test_save_to_file_failure():
    with patch("builtins.open", side_effect = Exception("error")):
        assert aac_to_text.save_to_file("test", "test.txt") is False

from unittest.mock import patch, MagicMock
import sys
sys.modules['whisper'] = MagicMock()
import aac_to_text

def test_transcribe_with_whisper_success():
    with patch("aac_to_text.whisper.load_model") as mock_load_model:
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model
        mock_model.transcribe.return_value = {"text": "test"}
        assert aac_to_text.transcribe_with_whisper("test.aac") == "test"


def test_save_to_file_success(tmp_path):
    output = tmp_path / "test.txt"
    aac_to_text.save_to_file("test", output)
    assert output.exists() is True
    assert output.read_text() == "test"

def test_save_to_file_failure():
    with patch("builtins.open", side_effect = Exception("error")):
        assert aac_to_text.save_to_file("test", "test.txt") is False

def test_convert_aac_to_text_file_not_exists():
    with patch("aac_to_text.os.path.exists", return_value=False):
        assert aac_to_text.convert_aac_to_text("test.aac") is False

def test_convert_aac_to_text_output_file_none():
    with patch("aac_to_text.os.path.exists", return_value=True), \
         patch("aac_to_text.transcribe_with_whisper", return_value="tekst"), \
         patch("aac_to_text.save_to_file", return_value=True) as mock_save:
        aac_to_text.convert_aac_to_text("nagranie.aac")
        mock_save.assert_called_once_with("tekst", "nagranie.txt")

def test_convert_aac_to_text_transcribe_failure():
    with patch("aac_to_text.os.path.exists", return_value=True), \
         patch("aac_to_text.transcribe_with_whisper", side_effect=Exception("error")):
        assert aac_to_text.convert_aac_to_text("nagranie.aac") is False 

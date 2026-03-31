import os
import sys
import argparse
import whisper
from pathlib import Path

def transcribe_with_whisper(audio_file):
    print(f"Loading Whisper model...")
    model = whisper.load_model("base")
    
    print(f"Transcribing file: {audio_file}")
    result = model.transcribe(audio_file, language="pl")
    
    return result["text"]


def save_to_file(text, output_file):

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Text saved to: {output_file}")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False


def convert_aac_to_text(audio_file, output_file=None):
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' does not exist")
        return False

    if output_file is None:
        output_file = Path(audio_file).stem + ".txt"
    
    print(f"Converting: {audio_file} -> {output_file}")
    print("-" * 50)

    try:
        text = transcribe_with_whisper(audio_file)
        print("-" * 50)
        print("Transcription complete!")
        print("\nResult:")
        print(text[:200] + "..." if len(text) > 200 else text)
    except Exception as e:
        print(f"Error: Transcription failed - {e}")
        return False

    if save_to_file(text, output_file):
        return True
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an audio file (.aac, .mp3, .wav) to text"
    )
    
    parser.add_argument(
        "input_file",
        help="Path to the audio file"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Path to the output file (default: input_file.txt)"
    )
    
    args = parser.parse_args()
    
    success = convert_aac_to_text(
        audio_file=args.input_file,
        output_file=args.output
    )
    
    sys.exit(0 if success else 1)

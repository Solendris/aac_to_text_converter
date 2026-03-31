import os
import sys
import argparse
import whisper
from pathlib import Path

def transcribe_with_whisper(audio_file):
    print(f"Ładowanie modelu Whisper...")
    model = whisper.load_model("base")
    
    print(f"Transkrybowanie pliku: {audio_file}")
    result = model.transcribe(audio_file, language="pl")
    
    return result["text"]


def save_to_file(text, output_file):

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Tekst zapisany do: {output_file}")
        return True
    except Exception as e:
        print(f"Błąd przy zapisywaniu pliku: {e}")
        return False


def convert_aac_to_text(audio_file, output_file=None):
    if not os.path.exists(audio_file):
        print(f"Błąd: Plik '{audio_file}' nie istnieje")
        return False

    if output_file is None:
        output_file = Path(audio_file).stem + ".txt"
    
    print(f"Konwersja: {audio_file} -> {output_file}")
    print("-" * 50)

    try:
        text = transcribe_with_whisper(audio_file)
        print("-" * 50)
        print("Transkrypcja zakończona!")
        print("\nWynik:")
        print(text[:200] + "..." if len(text) > 200 else text)
    except Exception as e:
        print(f"Błąd: Transkrypcja nie powiodła się - {e}")
        return False

    if save_to_file(text, output_file):
        return True
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Konwertuj plik audio (.aac, .mp3, .wav) na tekst"
    )
    
    parser.add_argument(
        "input_file",
        help="Ścieżka do pliku audio"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Ścieżka do pliku wyjściowego (domyślnie: input_file.txt)"
    )
    
    args = parser.parse_args()
    
    success = convert_aac_to_text(
        audio_file=args.input_file,
        output_file=args.output
    )
    
    sys.exit(0 if success else 1)

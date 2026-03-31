# AAC to Text Converter Script
# Konwersja pliku .aac na tekst za pomocą biblioteki Whisper

import os
import sys
import argparse
from pathlib import Path

# Metoda 1: Użycie OpenAI Whisper (polecane - darmowe, offline)
def transcribe_with_whisper(audio_file):
    """
    Transkrybuje plik audio do tekstu za pomocą OpenAI Whisper
    
    Wymagania:
    pip install openai-whisper
    Lub: pip install whisper
    """
    try:
        import whisper
    except ImportError:
        print("Błąd: Biblioteka 'whisper' nie jest zainstalowana.")
        print("Zainstaluj ją poleceniem: pip install openai-whisper")
        return None
    
    print(f"Ładowanie modelu Whisper...")
    # Dostępne modele: tiny, base, small, medium, large
    # tiny - najszybszy, najmniej dokładny
    # large - najwolniejszy, najbardziej dokładny
    model = whisper.load_model("base")
    
    print(f"Transkrybowanie pliku: {audio_file}")
    result = model.transcribe(audio_file, language="pl")
    
    return result["text"]


# Metoda 2: Użycie OpenAI API (wymaga API key)
def transcribe_with_openai_api(audio_file, api_key):
    """
    Transkrybuje plik audio do tekstu za pomocą OpenAI API
    
    Wymagania:
    pip install openai
    """
    try:
        from openai import OpenAI
    except ImportError:
        print("Błąd: Biblioteka 'openai' nie jest zainstalowana.")
        print("Zainstaluj ją poleceniem: pip install openai")
        return None
    
    client = OpenAI(api_key=api_key)
    
    print(f"Transkrybowanie pliku: {audio_file} (za pomocą OpenAI API)")
    
    with open(audio_file, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio
        )
    
    return transcript.text


# Metoda 3: Użycie Google Speech Recognition (dla krótkich plików)
def transcribe_with_google(audio_file):
    """
    Transkrybuje plik audio do tekstu za pomocą Google Speech Recognition
    
    Wymagania:
    pip install SpeechRecognition pydub
    """
    try:
        import speech_recognition as sr
        from pydub import AudioSegment
    except ImportError:
        print("Błąd: Wymagane biblioteki nie są zainstalowane.")
        print("Zainstaluj je poleceniem: pip install SpeechRecognition pydub")
        return None
    
    print(f"Ładowanie pliku audio: {audio_file}")
    
    # Załaduj plik audio
    sound = AudioSegment.from_file(audio_file)
    
    # Podziel na fragmenty po 60 sekund (Google ma limit czasu)
    chunk_length_ms = 60000
    chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]
    
    recognizer = sr.Recognizer()
    full_text = ""
    
    print(f"Transkrybowanie {len(chunks)} fragmentów audio...")
    
    for i, chunk in enumerate(chunks, 1):
        # Eksportuj fragment
        chunk_path = f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        
        # Transkrybuj fragment
        try:
            with sr.AudioFile(chunk_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="pl-PL")
                full_text += text + " "
                print(f"Fragment {i}: OK")
        except sr.UnknownValueError:
            print(f"Fragment {i}: Nie można zrozumieć")
        except sr.RequestError as e:
            print(f"Fragment {i}: Błąd API - {e}")
        finally:
            # Usuń tymczasowy plik
            if os.path.exists(chunk_path):
                os.remove(chunk_path)
    
    return full_text


def save_to_file(text, output_file):
    """Zapisuje tekst do pliku"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Tekst zapisany do: {output_file}")
        return True
    except Exception as e:
        print(f"Błąd przy zapisywaniu pliku: {e}")
        return False


def convert_aac_to_text(audio_file, output_file=None, method="whisper", api_key=None):
    """
    Główna funkcja do konwersji AAC na tekst
    
    Parametry:
    - audio_file: ścieżka do pliku audio (.aac, .mp3, .wav, etc.)
    - output_file: ścieżka do pliku wyjściowego (domyślnie: audio_file.txt)
    - method: metoda transkrypcji ("whisper", "openai", "google")
    - api_key: klucz API OpenAI (wymagany dla metody "openai")
    """
    
    # Sprawdzenie, czy plik istnieje
    if not os.path.exists(audio_file):
        print(f"Błąd: Plik '{audio_file}' nie istnieje")
        return False
    
    # Ustawienie domyślnej nazwy pliku wyjściowego
    if output_file is None:
        output_file = Path(audio_file).stem + ".txt"
    
    print(f"Konwersja: {audio_file} -> {output_file}")
    print(f"Metoda: {method}")
    print("-" * 50)
    
    # Wybór metody transkrypcji
    if method == "whisper":
        text = transcribe_with_whisper(audio_file)
    elif method == "openai":
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            print("Błąd: API key nie został podany")
            return False
        text = transcribe_with_openai_api(audio_file, api_key)
    elif method == "google":
        text = transcribe_with_google(audio_file)
    else:
        print(f"Błąd: Nieznana metoda '{method}'")
        return False
    
    if text is None:
        print("Błąd: Transkrypcja nie powiodła się")
        return False
    
    print("-" * 50)
    print("Transkrypcja zakończona!")
    print("\nWynik:")
    print(text[:200] + "..." if len(text) > 200 else text)
    
    # Zapis do pliku
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
    
    parser.add_argument(
        "-m", "--method",
        choices=["whisper", "openai", "google"],
        default="whisper",
        help="Metoda transkrypcji (domyślnie: whisper)"
    )
    
    parser.add_argument(
        "-k", "--api-key",
        help="Klucz API OpenAI (dla metody 'openai')"
    )
    
    args = parser.parse_args()
    
    success = convert_aac_to_text(
        audio_file=args.input_file,
        output_file=args.output,
        method=args.method,
        api_key=args.api_key
    )
    
    sys.exit(0 if success else 1)

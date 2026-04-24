from pathlib import Path
import subprocess
#import sounddevice as sd
#import soundfile as sf

BASE_DIR = Path(__file__).resolve().parent
piper_path = Path.home() / ".local" / "share" / "piper-tts" / "piper" / "piper"
model_path = BASE_DIR / "voices" / "en_US-ryan-medium.onnx"
config_path = BASE_DIR / "voices" / "en_US-ryan-medium.onnx.json"
out_file = BASE_DIR / "reply.wav"




def speak_text(text: str):
    # Step 1: generate the WAV with Piper
    subprocess.run(
        [
            str(piper_path),
            "--model", str(model_path),
            "--config", str(config_path),
            "--output_file", str(out_file),
        ],
        input=text,
        text=True,
        check=True
    )

    # Step 2: play it via Windows
    windows_path = subprocess.check_output(
        ["wslpath", "-w", str(out_file)],
        text=True
    ).strip()

    subprocess.run([
        "powershell.exe", "-c",
        f'Add-Type -AssemblyName presentationCore; '
        f'$player = New-Object System.Windows.Media.MediaPlayer; '
        f'$player.Open("{windows_path}"); '
        f'$player.Play(); '
        f'Start-Sleep -Seconds 10'
    ], check=True)
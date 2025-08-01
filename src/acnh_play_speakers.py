"""
Describe purpose of this script here

Created: 7/30/25
"""
from typing import Callable

import sounddevice as sd
import time

from acnh_state_machine import sample_rate, load_audio_files, load_chime, play_acnh, chunk_size


def main():
    # Start the audio stream
    try:
        audio_data = load_audio_files(n_files=1)
        chime = load_chime()
        print(sd.query_devices())
        stream = sd.OutputStream(
            samplerate=sample_rate,
            channels=2,
            callback=play_acnh(audio_data, chime),
            blocksize=chunk_size,
        )
        with stream:
            print("Playing loops with crossfades. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("Playback stopped.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

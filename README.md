# Animal Crossing: New Horizons Audio Player

## Overview

This Python script plays hourly background music with seamless looping and chime transitions, 
inspired by *Animal Crossing: New Horizons* (ACNH). It loads FLAC audio files for each hour, 
applies crossfading for smooth loops, and plays a chime at the end of each hour before 
switching tracks. The script currently functions as a local audio player using the 
`sounddevice` library, with plans to add streaming support in the future (Soon™).

## Features

- Plays 24 hourly background music tracks from `data/raw/` (e.g., `00.flac`, `01.flac`, etc.).
- Supports seamless looping with linear crossfading based on loop points defined in `data/loop_points.csv`.
- Transitions between hours with a 3-second fade-out and a chime (`data/chimes/Meekay I Chimes.ogg`).
- Configurable "hour" length for testing (default: 300 seconds; production: 3600 seconds).
- Uses a state machine to manage playback states (`STARTUP`, `NORMAL`, `FADEOUT`, `PLAYCHIME`).
- Audio output at 48kHz stereo with a block size of 1024 samples.

## Requirements

- **Python**: 3.11 or higher
- **Dependencies**:
  - `sounddevice`: For audio playback.
  - `soundfile`: For reading FLAC and OGG files.
  - `numpy`: For audio data manipulation.
- **Audio Files**:
  - Hourly tracks in `data/raw/` (e.g., `00.flac` to `23.flac`, 48kHz stereo).
  - Loop points in `data/loop_points.csv` (one integer per line, specifying the crossfade start sample).
    The included data/loop_points.csv works for the Animal Crossing New Horizons soundtrack that I have.
  - Chime file in `data/chimes/Meekay I Chimes.ogg` (48kHz).

Install dependencies using pip:
```bash
pip install -e .
```

## Setup

1. **Organize Audio Files**:
   - Place hourly FLAC files in `data/raw/` (named `00.flac` to `23.flac`).
   - Create `data/loop_points.csv` with loop points (one per line, in order of hours). The loop points are
     in *samples* from the beginning of the file to a point which matches the beginning of the file.
     As noted, the version in this project works fine for my copy of the soundtrack.
   - I will not help you rip the soundtrack.
   - Place the chime file in `data/chimes/Meekay I Chimes.ogg`.

2. **Directory Structure**:
   ```
   project_root/
   ├── data/
   │   ├── raw/
   │   │   ├── 00.flac
   │   │   ├── 01.flac
   │   │   └── ...
   │   ├── chimes/
   │   │   └── Meekay I Chimes.ogg
   │   └── loop_points.csv
   ├── acnh_audio_player.py
   └── README.md
   ```

3. **Verify Audio Files**:
   - Ensure all audio files are 48kHz stereo.
   - Confirm loop points in `loop_points.csv` are valid (less than the length of each audio file).

## Usage

Run the script with Python:
```bash
python acnh_audio_player.py
```

- The script plays music indefinitely, switching tracks every hour
- Press `Ctrl+C` to stop playback.
- Output is sent to the default audio device.

## Configuration

- **Hour Length**: Modify `hour_length` in the script (default: 300 seconds for testing; set to 3600 for real hours).
- **Volume**: Adjust `base_volume` in the `play_acnh` function (default: 0.1 to prevent clipping).
- **Debugging**: Set `debug_enabled = True` in `play_acnh` to enable logging of playback state and buffer details.

## Planned Features

- **Streaming Support (Soon™)**: The script will be extended to output audio to a virtual audio sink in a Docker container for streaming to platforms like Icecast or RTMP.

## Notes

- The script assumes 24 hourly tracks are available. If fewer tracks are provided, it cycles through them using modulo arithmetic.
- Timing accuracy is within one audio chunk (~21.33ms at 48kHz), sufficient for chime transitions.
- Ensure the audio device supports 48kHz stereo output to avoid errors.

## License

This project is unlicensed and provided as-is for personal use.

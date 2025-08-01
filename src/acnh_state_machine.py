"""
Describe purpose of this script here

Created: 7/31/25
"""
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable

import numpy as np
import sounddevice as sd
import soundfile as sf


@dataclass
class SongRecord:
    data:np.ndarray
    loop_crossfade_begin:int
    loop_crossfade_length:int
    filename:str


class PlaybackState(Enum):
    STARTUP=0
    NORMAL=1
    FADEOUT=2
    PLAYCHIME=3


sample_rate:int=48000 # All files must be at this rate, otherwise raise an erro
chunk_size:int=1024   # process samples in chunks of this size

def _make_loop(song:SongRecord,fade_samples:int):
    loopAchunk=song.data[:song.loop_crossfade_length,...].copy()
    loopBchunk=song.data[song.loop_crossfade_begin:song.loop_crossfade_begin+song.loop_crossfade_length,...].copy()
    fade_in=np.arange(song.loop_crossfade_length).reshape(-1,1)/fade_samples
    fade_out=1-fade_in
    loopAchunk[:]=loopAchunk*fade_in
    loopBchunk[:]=loopBchunk*fade_out
    song.data[song.loop_crossfade_begin:song.loop_crossfade_begin+song.loop_crossfade_length,...]=loopAchunk+loopBchunk
    song.data=song.data[:song.loop_crossfade_begin+song.loop_crossfade_length,...]
    return song


def load_audio_files(fade_time:float=1.0,n_files:int=24)->list[SongRecord]:
    audio_data = []
    fade_samples=int(fade_time*sample_rate)
    with open("data/loop_points.csv","rt") as inf:
        i_hour=0
        for line in inf:
            line=line.strip()
            if line=="":
                continue
            if line[0]=="#":
                continue
            loop_point=int(line)
            filename=f"data/snowy/{i_hour:02d}.flac"
            print(f"Loading {filename}")
            # Load all audio files and verify sample rate
            data, fs = sf.read(filename)
            if fs != sample_rate:
                raise ValueError(f"File {filename} has sample rate {fs}, expected {sample_rate}")
            if loop_point >= len(data):
                raise ValueError(f"Loop point {loop_point} exceeds length of {filename}")
            audio_data.append(_make_loop(song=SongRecord(data=data,
                                                         loop_crossfade_begin=loop_point,
                                                         loop_crossfade_length=fade_samples,
                                                         filename=filename),
                                                         fade_samples=fade_samples))
            i_hour+=1
            if i_hour>=n_files:
                break
    return audio_data


def load_chime(volume:float=0.3,tfade0:float=15.0,tfade1:float=18.0)->SongRecord:
    filename = f"data/chimes/Meekay I Chimes.ogg"
    print(f"Loading {filename}")
    # Load all audio files and verify sample rate
    data, fs = sf.read(filename)
    if fs != sample_rate:
        raise ValueError(f"File {filename} has sample rate {fs}, expected {sample_rate}")
    # Modify samples.
    sample1=int(tfade1*fs)
    data=data[:sample1,...]
    t=np.linspace(0,tfade1,int(tfade1*fs))
    volumes=np.interp(t,[tfade0,tfade1],[volume,0.0],left=volume,right=0.0).reshape(-1,1)
    data*=volumes
    # ensure an integer number of chunks
    data=data[:chunk_size*(data.shape[0]//chunk_size),...]

    return SongRecord(data=data,
                      loop_crossfade_begin=None,
                      loop_crossfade_length=None,
                      filename=filename)


def play_acnh(songs:list[SongRecord],chime:SongRecord,hour_length:int=3600)->Callable[[np.ndarray,int,'CData',sd.CallbackFlags],None]:
    def get_current_hour():
        return int(time.localtime().tm_hour)
    def get_seconds_of_hour():
        return time.time() % hour_length
    calls=0
    current_sample=0 #Note that this will play the original un-faded intro
    state=PlaybackState.STARTUP
    songdata=None
    N=0
    loopstart=0
    def inner(outdata:np.ndarray, frames:int, time:'CData', status:sd.CallbackFlags)->None:
        nonlocal calls,current_sample,state,songdata,N,loopstart
        calls+=1
        if state==PlaybackState.STARTUP:
            # Fresh start, figure out hour
            current_sample=0
            current_hour=get_current_hour()%len(songs)
            song=songs[current_hour]
            print(f"Switching to song {current_hour}: {song.filename}")
            songdata=song.data
            loopstart=song.loop_crossfade_length
            N=songdata.shape[0]
            state=PlaybackState.NORMAL
            volume=1.0
        elif state==PlaybackState.NORMAL:
            volume=1.0
            # Check if in final 3 seconds
            if get_seconds_of_hour()>(hour_length-3):
                print("Starting fadeout")
                state=PlaybackState.FADEOUT
        elif state==PlaybackState.FADEOUT:
            fadeleft=(hour_length-get_seconds_of_hour())/3
            if fadeleft>1:
                volume=0.0
                print("Playing top of hour chime")
                state=PlaybackState.PLAYCHIME
                songdata=chime.data
                N=songdata.shape[0]
                current_sample=0
            else:
                volume=fadeleft
        elif state==PlaybackState.PLAYCHIME:
            volume=1.0
            if (N-current_sample)<chunk_size*2:
                print("Done playing top of hour chime")
                state=PlaybackState.STARTUP

        samples_left = N - current_sample

        samples_A = min(frames, samples_left)
        samples_B = frames-samples_A
        outdata[0:samples_A,...] = songdata[current_sample:current_sample+samples_A,...]
        if samples_B>0:
            outdata[samples_A:samples_A + samples_B, ...] = songdata[
                                                              loopstart:
                                                              loopstart + samples_B,
                                                            ...]
            current_sample=loopstart+samples_B
            print(f"Looping, {samples_B} samples from beginning of loop")
        else:
            current_sample += samples_A
        outdata*=volume
        #delta=time.outputBufferDacTime-time.currentTime

    return inner

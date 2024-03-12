
import mido
from mido import MidiFile
import matplotlib.pyplot as plt
import librosa
import librosa.display
import pretty_midi
import numpy as np
import streamlit as st


def plot_waveform(audio_path, save_path='graph_images/wave.png'):
    y, sr = librosa.load(audio_path, sr=None)
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(y=y, sr=sr, color='#bda22d')
    plt.title('Audio Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_midi_notes_with_labels(midi_file):
    file_like_object = midi_file
    midi_data = pretty_midi.PrettyMIDI(file_like_object)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(midi_data.instruments)))
    for instrument, color in zip(midi_data.instruments, colors):
        for note in instrument.notes:
            note_start = note.start
            note_end = note.end
            note_pitch = note.pitch
            ax.plot([note_start, note_end], [note_pitch, note_pitch], color=color, linewidth=2)
        if instrument.is_drum:
            ax.plot([], [], color=color, label="Percussion (Drums)")
        else:
            instrument_name = pretty_midi.program_to_instrument_name(instrument.program)
            ax.plot([], [], color=color, label=instrument_name)
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('MIDI note number')
    ax.legend(loc='upper right')
    ax.set_title('MIDI Notes Visualization')
    st.pyplot(fig)

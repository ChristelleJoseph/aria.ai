import streamlit as st
st.set_page_config(
    page_title='Aria.ai',
    page_icon= "🎧"
)

import streamlit as st
import sys
import os

if 'streamlit' in os.environ:
    current_dir = os.getcwd()
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importing after adding the parent directory to the path
from model.predict import generate
import matplotlib.pyplot as plt
from mido import MidiFile
from music21 import instrument
import pretty_midi
import io
import numpy as np
import tempfile
from midi2audio import FluidSynth
import librosa
import librosa.display
from plots import plot_midi_notes_with_labels, plot_waveform


def generate_colored_text(text, colors):
    return "".join(
        f"<span style='color: {colors[i % len(colors)]}; font-size: 75px; font-weight: bold;'>{char}</span>"
        for i, char in enumerate(text)
    )

def align_text(text, alignment='left'):
    return f"<div style='text-align: {alignment};'>{text}</div>"

def add_bg_from_url(img, position='center'):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url({img});
            background-size: auto;
            background-position: {position};
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True)


def show():
    rainbow_colors = ['#693C72', '#C15050', '#D97642', '#337357', '#D49D42']
    title = "Aria.ai 🎹"
    notes = "♩♫♪"
    colored_title = generate_colored_text(title, rainbow_colors)
    st.markdown(align_text(colored_title, 'left'), unsafe_allow_html=True)
    st.write('A lean learning Machine')

    img = """
    https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDlodmtyM3VjczRkNnNpemFhZ3ZsMXl0Mjg3ZXJhZHF6OHI1ODczbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/D3vTKclRSaLxT7YlUT/giphy.gif
    """
    add_bg_from_url(img)
    col1, col2 = st.columns(2)
    with col1:
        lead_instrument_option = st.selectbox(
            "Select lead instrument:",
            ['Piano', 'Guitar'],
            index=0,
            key='lead_instrument_selectbox'
        )

    with col2:
        st.write("Add accompanying instruments:")
        drums = st.checkbox("Drums", key="drums")
        banjo = st.checkbox("Banjo", key="banjo")

    if 'lead_instrument' not in st.session_state:
        st.session_state['lead_instrument'] = None
    if 'additional_instruments' not in st.session_state:
        st.session_state['additional_instruments'] = []

    st.session_state['lead_instrument'] = instrument.Piano() if lead_instrument_option == 'Piano' else instrument.ElectricGuitar()
    st.session_state['additional_instruments'] = []
    if drums:
        st.session_state['additional_instruments'].append('Drums')
    if banjo:
        st.session_state['additional_instruments'].append('Banjo')

    # Generating music...
    import time
    if st.button('Generate Music'):
        placeholder = st.empty()
        placeholder.text("Generating Music...")
        for i in range(40):
            placeholder.text(f"Generating Music{'.' * (i % 4 + 1)}")
            time.sleep(0.1)  # Adjusted for example, consider your actual generation time
        # Call the generate function with the selected instruments
        add_parts = st.session_state['additional_instruments']

        col1, col2, col3 = st.columns([1, 2, 4])
        with col3:
            fun_fact = st.empty()
            fun_fact.success("""
                             Named 'Aria' in honor of the exquisite solos that grace operas and the boldness of Arya Stark,
                             this title reflects the synergy between artistic finesse and the smart intricacies of the LSTM model.

                             """)

        generate(
            lead_instrument=st.session_state['lead_instrument'],
            add_parts=add_parts
        )

        placeholder.text("Music generation complete!")
        fun_fact.empty()

        add_bg_from_url(img, position='top right')
        midi_file = os.path.join('music_output', 'output.mid')
        st.title("Visual Midi Output")
        plot_midi_notes_with_labels(midi_file)


        # Convert Original MIDI to WAV
        soundfont_path_1 = os.path.join(current_dir, 'soundfonts', 'Rocchetta.sf2')
        fs = FluidSynth(soundfont_path_1)
        fs.midi_to_audio(midi_file, 'music_output/output.wav')
        audio_path = 'music_output/output.wav'

        plot_waveform(audio_path)
        st.audio(audio_path)
        st.image('graph_images/wave.png')

        # Convert Original MIDI to EDM WAV
        soundfont_path_2 = os.path.join(current_dir, 'soundfonts', 'ClubSawHD.sf2')
        fs = FluidSynth(soundfont_path_2)
        fs.midi_to_audio(midi_file, 'music_output/output_techno.wav')
        edm_track = 'music_output/output_techno.wav'
        st.title("EDM-ify")
        st.audio(edm_track)


footer="""<style>
.a {
    position: fixed;
    left: 0;
    bottom: 10px;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
<div class="a">Made with ❤️ by Christelle J </div>
"""
st.markdown(footer,unsafe_allow_html=True)


if __name__ == "__main__":
    show()

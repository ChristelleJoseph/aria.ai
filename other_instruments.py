
from music21 import tempo, instrument, note, chord, stream, percussion, duration

def create_hard_drum_track(measures, tempo=120):
    drum_part = stream.Part()
    drum_part.append(instrument.SnareDrum())  # Set the part as a percussion instrument

    # Define the drum pattern for each measure
    for measure in range(measures):
        for beat in range(4):  # Assuming a 4/4 time signature
            # Add a bass drum on beats 1 and 3
            if beat in [0, 2]:
                bass_drum = note.Note()
                bass_drum.pitch.midi = 36  # MIDI note for Acoustic Bass Drum
                bass_drum.duration = duration.Duration(1)  # One beat long
                drum_part.insert(measure * 4 + beat, bass_drum)

            # Add a snare drum on beats 2 and 4
            if beat in [1, 3]:
                snare_drum = note.Note()
                snare_drum.pitch.midi = 38  # MIDI note for Acoustic Snare
                snare_drum.duration = duration.Duration(1)
                drum_part.insert(measure * 4 + beat, snare_drum)

    return drum_part

def create_Banjo_track(measures=16, spread=0):
    # Create a Stream for the banjo part
    banjo_part = stream.Part()
    banjo_part.insert(0, instrument.Banjo())

    # Define a chord progression in C major: I-V-vi-IV
    chords = [
        ['C', 'E', 'G'],  # C Major
        ['G', 'B', 'D'],  # G Major
        ['A', 'C', 'E'],  # A Minor
        ['F', 'A', 'C']   # F Major
    ]
    # Iterate over the measures
    for i in range(measures):
        # Pick a note from the current chord, cycling through the notes in the chord
        current_chord = chords[i % len(chords)]
        note_name = current_chord[i % len(current_chord)]  # Cycle through notes within the chord
        # Create a note
        n = note.Note(note_name)
        n.duration = duration.Duration("whole")  # Change duration as needed
        banjo_part.append(n)

    return banjo_part

""" This module generates notes for a midi file using the
    trained neural network """
import pickle
import numpy
from music21 import tempo, instrument, note, chord, stream, percussion, duration
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import BatchNormalization as BatchNorm
from keras.layers import Activation
from music21 import stream, note, duration, instrument
from music21 import stream, chord, note
from other_instruments import create_hard_drum_track, create_Banjo_track

def generate(lead_instrument, add_parts):
    """ Generate a piano midi file """
    print('I got called')
    #load the notes used to train the model
    with open('data/notes', 'rb') as filepath:
        notes = pickle.load(filepath)

    # Get all pitch names
    pitchnames = sorted(set(item for item in notes))
    # Get all pitch names
    n_vocab = len(set(notes))

    network_input, normalized_input = prepare_sequences(notes, pitchnames, n_vocab)
    model = create_network(normalized_input, n_vocab)
    prediction_output = generate_notes(model, network_input, pitchnames, n_vocab)
    create_midi(prediction_output, lead_instrument=lead_instrument, add_parts=add_parts)


def prepare_sequences(notes, pitchnames, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    # map between notes and integers and back
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    sequence_length = 32
    network_input = []
    output = []
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    normalized_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    normalized_input = normalized_input / float(n_vocab)

    return (network_input, normalized_input)

def create_network(network_input, n_vocab):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        recurrent_dropout=0.3,
        return_sequences=True
    ))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(LSTM(512))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    # Load the weights to each node
    model.load_weights('weights/weights-improvement-01-0.3844.keras')


    return model

def generate_notes(model, network_input, pitchnames, n_vocab):
    """ Generate notes from the neural network based on a sequence of notes """
    # pick a random sequence from the input as a starting point for the prediction
    start = numpy.random.randint(0, len(network_input)-1)

    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    pattern = network_input[start]
    prediction_output = []

    # generate 500 notes
    for note_index in range(200):
        prediction_input = numpy.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)

        index = numpy.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]

    return prediction_output


def create_midi(prediction_output, output_filename='output.mid', lead_instrument=instrument.AcousticGuitar(), add_parts=[]):
    """Convert the output from the prediction to notes and create a midi file
    from the notes, with adjustments for techno music."""

    offset = 0
    output_notes = []
    # instrument_ = instrument.Instrument(midiProgram=82)
    # lead_instrument = instrument.Instrument()
    # lead_instrument.midiProgram = 55
    lead_instrument = lead_instrument

    def add_note_or_chord(pattern, offset):
        """Helper function to add a note or chord to the output_notes list."""
        if ('.' in pattern) or pattern.isdigit():  # pattern is a chord
            notes_in_chord = [note.Note(int(n)) for n in pattern.split('.')]
            new_chord = chord.Chord(notes_in_chord)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:  # pattern is a note
            new_note = note.Note(pattern)
            new_note.offset = offset
            output_notes.append(new_note)

    # Create note and chord objects based on the values generated by the model
    for pattern in prediction_output:
        add_note_or_chord(pattern, offset)
        offset += 0.5

    total_measures = int(len(prediction_output) * 0.5 / 4)

    melody_stream = stream.Stream(output_notes)
    final_stream = stream.Stream()
    melody_stream.insert(0, lead_instrument)
    if 'Drums' in add_parts:
        drum_part = create_hard_drum_track(measures=total_measures)
        final_stream.append(drum_part)
    # if 'Banjo' in add_parts:
    #     banjo_part = create_Banjo_track(measures=total_measures)
    #     final_stream.append(banjo_part)
    # final_stream.append(melody_stream)
    final_stream.write('midi', fp=output_filename)

if __name__ == '__main__':
    generate(lead_instrument=instrument.AcousticGuitar(), add_parts=None)

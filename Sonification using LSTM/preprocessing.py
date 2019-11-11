from music21 import *
import glob
import sys
import numpy as np
import os
import logging
from fnmatch import fnmatch
import torch 

#Create a Logging File
logging.basicConfig(filename="test.log", level=logging.DEBUG)

#This function is to simplify the midi file and extract the right hand notes from the midi file
def extract_right_notes(file_path):
    #Intializing empty set
    notes = {}
    #Check if the input path is a file or not
    notes = get_notes(file_path)
    # print(notes)    
    create_midi(notes, file_path)
    return notes
#Get all the notes and highest note from each cord from the midi files 
def get_notes(filename):
    #Read the midi file
    midi = converter.parse(filename)
    notes_i = []
    notes_pitch=[]
    notes_to_parse = None
    logging.debug("File that is being parsed currently is {}".format(filename))
    
    try: 
        # Extracting the instrument parts
        notes_to_parse = midi[0].recurse()
    
    except: 
        # Extracting the notes in a flat structure
        notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes_i.append(str(element.pitch))
            notes_pitch.append(str(element.pitch.midi))
        elif isinstance(element, chord.Chord):
            # Taking the note with the highest octave.
            notes_i.append(str(element.pitches[-1])) 
            notes_pitch.append(str(element.pitches[-1].midi))
    # print(notes_i)
    # print(notes_pitch)
    return notes_i
    #return notes
def create_midi(melody, filename):
    """ create a midi file from the notes """
    offset = 0
    output_notes = []
    # create note and chord objects based on the values generated by the model
    for pattern in melody:
        # pattern is a note
        try:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)
            # increase offset each iteration so that notes do not stack
            offset += 0.5
        except:
            logging.debug('Exception thrown, note not appended')

    midi_stream = stream.Stream(output_notes)
    cwd=os.getcwd()
    cwd="\\".join(str(cwd).split("\\")[:-1])
    filename = str(filename.split("\\")[-1])
    if(os.path.exists(os.path.join(cwd,"Training_Data"))):
        pass
    else:
        os.makedirs(os.path.join(cwd,"Training_Data"))
    midi_stream.write('midi', fp=os.path.join(cwd,'Training_Data',filename))
def number_of_output_notes_generated(notes):
    all_notes=[]
    for item in notes:
        all_notes.extend(item)
    number_of_output_notes=len(set(all_notes))
    return number_of_output_notes

def generate_training_data(notes,number_of_output_notes_generated):
    sequence_length=50
    notes_from_training_data = []
    
    for item in notes:
        notes_from_training_data.extend(item)

    # get all right hand note names
    right_hand_notes = sorted(set(item for item in notes_from_training_data))
    # for i in range(len(right_hand_notes)):
    #     right_hand_notes[i]=str(right_hand_notes[i]).replace("-","#")
     # create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(right_hand_notes))
    print(note_to_int)
    int_to_note={note:ii for ii,note in note_to_int.items()}
    # print(int_to_note)
    network_input = []
    network_output = []
    for song in notes:
        for i in range(0, len(song) - sequence_length, 1):
            sequence_in = song[i:i + sequence_length]
            sequence_out = song[i + sequence_length]
            network_input.append([note_to_int[char] for char in sequence_in])
            network_output.append(note_to_int[sequence_out])
    assert len(network_input) == len(network_output), len(network_input)
    # network_input=[network_i/float(number_of_output_notes_generated) for network_i in network_input]
    network_input=np.array(network_input)
    n_patterns = len(network_input)
    # reshape the input into a format compatible with LSTM layers
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    network_input=network_input/float(number_of_output_notes_generated)
    # network_output = np_utils.to_categorical(network_output)
    # print(network_output)
    # print(network_input)
    return (network_input, network_output)

def one_hot_encode(arr, n_labels):
    
    # Initialize the the encoded array
    one_hot = np.zeros((arr.size, n_labels), dtype=np.float32)
    
    # Fill the appropriate elements with ones
    one_hot[np.arange(one_hot.shape[0]), arr.flatten()] = 1.
    
    # Finally reshape it to get back to the original array
    one_hot = one_hot.reshape((*arr.shape, n_labels))
    
    return one_hot


def preprocess_notes(path):
    # path=sys.argv[1]
    pattern = "*.mid"
    notes=[]
    if not path.endswith(".mid"):
        for path, subdirs, files in os.walk(path):
            for name in files:
                if fnmatch(name, pattern):
                    notes.append(extract_right_notes(os.path.join(path, name)))
    else:        
        notes.append(extract_right_notes(path))
    number_of_output_notes=number_of_output_notes_generated(notes)
    network_input,network_output=generate_training_data(notes,number_of_output_notes)
    network_input=torch.tensor(network_input)
    network_output=torch.tensor(network_output)

    return network_input,network_output

if __name__=="__main__":
    input_tensor,output_tensor=preprocess_notes("D:\Prem\Sem1\MM in AI\Project\Project\Sonification-using-Deep-Learning\Dataset")
    # print(input_tensor)

import os

class MidiNotesMapping():


    def get_midi_number_notes_mapping(self,file_name):
        '''
        

        Parameters:
            - file_name (float) :

        Returns:
            -  A dictionary

        '''
        note_to_midi_mapping = {}

        with open(file_name) as f:
            for line in f:
                (midi_value, notes) = line.split()
                note_to_midi_mapping[int(midi_value)] = notes
        return note_to_midi_mapping
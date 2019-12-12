class MidiClassMapping():
    def __init__(self):
        self.midi_list=[]
        self.note_to_int={}
        self.int_to_note={}
        self.max_midi_value=0
        self.min_midi_value=0
    def midi_notes_to_class_mapping(self,notes,midi_notes_mapping):        
        for note in notes:
            for midi,note_value in midi_notes_mapping.items():
                if str(note) in note_value:
                    self.midi_list.append(midi)
        # self.midi_list=sorted(notes)
        self.max_midi_value=self.midi_list[len(self.midi_list)-1]
        self.min_midi_value=self.midi_list[0]
        self.note_to_int = dict((note, number) for number, note in enumerate(self.midi_list))
        self.int_to_note={note:ii for ii,note in self.note_to_int.items()}
        return self.note_to_int,self.int_to_note,self.max_midi_value,self.min_midi_value
if __name__=="__main__":
    midi_class_object=MidiClassMapping()
    midi_notes_mapping={127: 'G9', 126: 'F#9/G-9', 125: 'F9', 124: 'E9', 123: 'D#9/E-9', 122: 'D9', 121: 'C#9/D-9', 120: 'C9', 119: 'B8', 118: 'A#8/B-8', 117: 'A8', 116: 'G#8/A-8', 115: 'G8', 114: 'F#8/G-8', 113: 'F8', 112: 'E8', 111: 'D#8/E-8', 110: 'D8', 109: 'C#8/D-8', 108: 'C8', 107: 'B7', 106: 'A#7/B-7', 105: 'A7', 104: 'G#7/A-7', 103: 'G7', 102: 'F#7/G-7', 101: 'F7', 100: 'E7', 99: 'D#7/E-7', 98: 'D7', 97: 'C#7/D-7', 96: 'C7', 95: 'B6', 94: 'A#6/B-6', 93: 'A6', 92: 'G#6/A-6', 91: 'G6', 90: 'F#6/G-6', 89: 'F6', 88: 'E6', 87: 'D#6/E-6', 86: 'D6', 85: 'C#6/D-6', 84: 'C6', 83: 'B5', 82: 'A#5/B-5', 81: 'A5', 80: 'G#5/A-5', 79: 'G5', 78: 'F#5/G-5', 77: 'F5', 76: 'E5', 75: 'D#5/E-5', 74: 'D5', 73: 'C#5/D-5', 72: 'C5', 71: 'B4', 70: 'A#4/B-4', 69: 'A4', 68: 'G#4/A-4', 67: 'G4', 66: 'F#4/G-4', 65: 'F4', 64: 'E4', 63: 'D#4/E-4', 62: 'D4', 61: 'C#4/D-4', 60: 'C4', 59: 'B3', 58: 'A#3/B-3', 57: 'A3', 56: 'G#3/A-3', 55: 'G3', 54: 'F#3/G-3', 53: 'F3', 52: 'E3', 51: 'D#3/E-3', 50: 'D3', 49: 'C#3/D-3', 48: 'C3', 47: 'B2', 46: 'A#2/B-2', 45: 'A2', 44: 'G#2/A-2', 43: 'G2', 42: 'F#2/G-2', 41: 'F2', 40: 'E2', 39: 'D#2/E-2', 38: 'D2', 37: 'C#2/D-2', 36: 'C2', 35: 'B1', 34: 'A#1/B-1', 33: 'A1', 32: 'G#1/A-1', 31: 'G1', 30: 'F#1/G-1', 29: 'F1', 28: 'E1', 27: 'D#1/E-1', 26: 'D1', 25: 'C#1/D-1', 24: 'C1', 23: 'B0', 22: 'A#0/B-0', 21: 'A0'}
    notes=['G9','G8','A7','A5']
    note_to_int,int_to_note,max_value,min_value=midi_class_object.midi_notes_to_class_mapping(notes,midi_notes_mapping)
    print(note_to_int)
    print(int_to_note)
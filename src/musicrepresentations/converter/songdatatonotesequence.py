import copy
import note_seq

class SongDataToNoteSequenceConverter:

    def convert(song_data:dict, quantize_steps_per_quarter=8, remove_disabled_tracks=True):

        # Clone the song data.
        song_data = copy.deepcopy(song_data)

        # Sort the tracks by instrument.
        tracks = sorted(song_data["tracks"], key=lambda t: t["instrument"])
        song_data["tracks"] = tracks

        # Remove tracks that are not enabled.
        if remove_disabled_tracks:
            song_data["tracks"] = [t for t in song_data["tracks"] if t.get("enabled", True)]

        # Create an empy note sequence.
        note_sequence = note_seq.protobuf.music_pb2.NoteSequence()

        # Add the tempo.
        bpm = song_data["bpm"] if "bpm" in song_data else 120
        note_sequence.tempos.add().qpm = bpm

        # Compute some lengths.
        step_length_seconds = 60.0 / bpm / quantize_steps_per_quarter
        bar_length_seconds = 4 * step_length_seconds * quantize_steps_per_quarter

        # Get the instruments.
        instruments = list(set([t["instrument"] for t in song_data["tracks"]]))

        # Add the tracks.
        for track_index, track_data in enumerate(song_data["tracks"]):
            instrument = track_data["instrument"]
            for bar_index, bar_data in enumerate(track_data["bars"]):
                bar_start_time = bar_index * bar_length_seconds
                for note_data in bar_data["notes"]:
                    assert "note" in note_data
                    assert "start" in note_data
                    assert "end" in note_data
                    note = note_sequence.notes.add()
                    #note.instrument = instrument TODO
                    note.pitch = note_data["note"]
                    note.start_time = note_data["start"] * step_length_seconds + bar_start_time
                    note.end_time = note_data["end"] * step_length_seconds + bar_start_time
                    note.velocity = 80
                    note.instrument = track_index
                    if instrument == "drums":
                        note.is_drum = True
                    else:
                        note.is_drum = False
                        note.program = int(instrument)

        return note_sequence
    

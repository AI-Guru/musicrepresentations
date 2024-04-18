

class TokensToSongDataConverter:
    """
    Converts a token sequence to song data.
    """

    def convert(token_sequence:str):
        tokens = token_sequence.split(" ")
        assert tokens[0] == "PIECE_START", f"Invalid token sequence: {token_sequence}"

        track_start_indices = [i for i, token in enumerate(tokens) if token == "TRACK_START"]
        track_end_indices = [i for i, token in enumerate(tokens) if token == "TRACK_END"]

        # Create the song data.
        song_data = {
            "tracks": []
        }
        for track_start_index, track_end_index in zip(track_start_indices, track_end_indices):
            track_string = " ".join(tokens[track_start_index:track_end_index+1])
            track_data = TokensToSongDataConverter.convert_track_tokens(track_string)
            song_data["tracks"].append(track_data)
        return song_data


    def convert_track_tokens(token_sequence:str):
            
        # Split the token sequence into tokens.
        tokens = token_sequence.split(" ")

        assert tokens[0] == "TRACK_START", f"Invalid token sequence: {token_sequence}"
        assert tokens[-1] == "TRACK_END", f"Invalid token sequence: {token_sequence}"

        # Create the track data.
        track_data = {
            "instrument": None,
            "bars": []
        }

        # Iterate through the tokens.
        current_instrument = None
        current_bar_tokens = []
        for token in tokens:

            # Track start.
            if token == "TRACK_START":
                pass

            # Instrument.
            elif token.startswith("INST="):
                current_instrument = token.split("=")[1].lower()
                track_data["instrument"] = current_instrument

            # Bar start.
            elif token == "BAR_START":
                current_bar_tokens = ["BAR_START"]

            # Bar end.
            elif token == "BAR_END":
                current_bar_tokens.append("BAR_END")
                bar_data = TokensToSongDataConverter.convert_bar_tokens(" ".join(current_bar_tokens))
                track_data["bars"].append(bar_data)

            # Other.
            else:
                current_bar_tokens.append(token)

        return track_data
    

    def convert_bar_tokens(token_sequence:str):

        # Split the token sequence into tokens.
        tokens = token_sequence.split(" ")

        assert tokens[0] == "BAR_START", f"Invalid token sequence: {token_sequence}"
        assert tokens[-1] == "BAR_END", f"Invalid token sequence: {token_sequence}"

        # Create the bar data.
        bar_data = {
            "notes": []
        }

        # Iterate through the tokens.
        current_time = 0
        current_notes = []
        for token in tokens:

            # Bar start.
            if token == "BAR_START":
                pass

            elif token.startswith("DENSITY="):
                density = int(token.split("=")[1])
                bar_data["density"] = density

            # Starts a new note.
            elif token.startswith("NOTE_ON="):
                note = {
                    "note": int(token.split("=")[1]),
                    "start": current_time,
                    "end": current_time + 1
                }
                current_notes.append(note)
                bar_data["notes"].append(note)

            # Passes time.
            elif token.startswith("TIME_DELTA="):
                current_time += int(token.split("=")[1])
            
            # Ends a note.
            elif token.startswith("NOTE_OFF="):
                note = [n for n in current_notes if n["note"] == int(token.split("=")[1])][0]
                note["end"] = current_time
                current_notes.remove(note)

            # Ends the bar.
            elif token.startswith("BAR_END"):
                pass
            else:
                raise Exception(f"Invalid token: {token} in token sequence: {token_sequence}")
        assert len(current_notes) == 0, f"Current notes is not empty: {current_notes}"

        return bar_data
    

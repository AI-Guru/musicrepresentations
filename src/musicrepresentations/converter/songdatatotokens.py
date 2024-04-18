

class SongDataToTokensConverter:

    def convert_track_data(track_data:dict):

        assert "instrument" in track_data, f"Invalid track data: {track_data}"
        assert "bars" in track_data, f"Invalid track data: {track_data}"

        instrument = track_data["instrument"]
        bars = track_data["bars"]

        # Create the token sequence.
        token_sequence = []
        token_sequence += ["TRACK_START"]
        token_sequence += [f"INST={instrument.upper()}"]

        # Add the bars.
        for bar in bars:
            bar_data_token_sequence = SongDataToTokensConverter.convert_bar_data(bar)
            token_sequence += bar_data_token_sequence.split(" ")

        # Add the end token.
        token_sequence += ["TRACK_END"]

        token_sequence = " ".join(token_sequence)
        return token_sequence


    def convert_bar_data(bar_data:dict):
        assert "notes" in bar_data, f"Invalid bar data: {bar_data}"

        notes = bar_data["notes"]

        if len(notes) == 0:
            token_sequence = []
            token_sequence += ["BAR_START"]
            token_sequence += [f"DENSITY={bar_data['density']}"]
            token_sequence += ["BAR_END"]
            return " ".join(token_sequence)

        # Check if the notes are fine.
        for note in notes:
            assert "note" in note, f"Invalid note: {note}"
            assert "start" in note, f"Invalid note: {note}"
            assert "end" in note, f"Invalid note: {note}"

        # Sort the notes by start time.
        notes = sorted(notes, key=lambda n: n["start"])

        # Find the maximum end and start time.
        max_end_time = max([n["end"] for n in notes])
        max_start_time = max([n["start"] for n in notes])
        max_time = max(max_end_time, max_start_time)
        del max_end_time
        del max_start_time

        # Create an events list.
        events = [[] for _ in range(max_time + 1)]

        # Add the notes to the events.
        for note in notes:
            events[note["start"]].append(f"NOTE_ON={note['note']}")
            events[note["end"]].append(f"NOTE_OFF={note['note']}")

        # Create the token sequence.
        token_sequence = []
        token_sequence += ["BAR_START"]

        # Add the density.
        if "density" in bar_data:
            token_sequence += [f"DENSITY={bar_data['density']}"]

        # Add the events.
        time_delta = 0
        for time_index, events in enumerate(events):

            if len(events) > 0:
                if time_delta > 0:
                    token_sequence += [f"TIME_DELTA={time_delta}"]
                time_delta = 0
                token_sequence += events

            time_delta += 1

        # Add the end token.
        token_sequence += ["BAR_END"]

        token_sequence = " ".join(token_sequence)
        return token_sequence

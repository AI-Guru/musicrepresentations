class LlmDataToTokensConverter:

    def convert(llmdata:str):
        llmdata = llmdata.split(" ")
        
        new_tokens = []
        in_track = False
        in_bar = False
        while len(llmdata) > 0:
            token = llmdata.pop(0)

            # "piece start" -> "PIECE_START
            if token == "piece":
                next_token = llmdata.pop(0)
                if next_token != "start":
                    raise Exception(f"Expected 'start' but got '{next_token}'")
                new_tokens.append("PIECE_START")

            # "track start" -> "TRACK_START"
            # "track end" -> "TRACK_END"
            elif token == "track":
                next_token = llmdata.pop(0)
                if not in_track and next_token != "start":
                    raise Exception(f"Expected 'start' but got '{next_token}'")
                if in_track and next_token != "end":
                    raise Exception(f"Expected 'end' but got '{next_token}'")

                if next_token == "start":
                    new_tokens.append("TRACK_START")
                    in_track = True
                if next_token == "end":
                    new_tokens.append("TRACK_END")
                    in_track = False

            # "inst NUMBER" -> "INST=NUMBER"
            elif token == "inst":
                next_token = llmdata.pop(0)
                new_tokens.append(f"INST={next_token}")

            # "bar start" -> "BAR_START"
            # "bar end" -> "BAR_END"
            elif token == "bar":
                next_token = llmdata.pop(0)
                if not in_bar and next_token != "start":
                    raise Exception(f"Expected 'start' but got '{next_token}'")
                if in_bar and next_token != "end":
                    raise Exception(f"Expected 'end' but got '{next_token}'")

                if next_token == "start":
                    new_tokens.append("BAR_START")
                    in_bar = True
                if next_token == "end":
                    new_tokens.append("BAR_END")
                    in_bar = False

            # "density NUMBER" -> "DENSITY=NUMBER"
            elif token == "density":
                next_token = llmdata.pop(0)
                new_tokens.append(f"DENSITY={next_token}")

            # "on NUMBER" -> "NOTE_ON=NUMBER"
            elif token == "on":
                next_token = llmdata.pop(0)
                new_tokens.append(f"NOTE_ON={next_token}")

            # "delta NUMBER" -> "TIME_DELTA=NUMBER"
            elif token == "delta":
                next_token = llmdata.pop(0)
                new_tokens.append(f"TIME_DELTA={next_token}")

            # "off NUMBER" -> "NOTE_OFF=NUMBER"
            elif token == "off":
                next_token = llmdata.pop(0)
                new_tokens.append(f"NOTE_OFF={next_token}")

            else:
                raise Exception(f"Invalid token: {token}")


        return " ".join(new_tokens)



import copy
import note_seq
    

def check_token_sequence_equality(token_sequence_1, token_sequence_2):
    # Split the token sequences into tokens.
    tokens_1 = token_sequence_1.split(" ")
    tokens_2 = token_sequence_2.split(" ")

    equal_list = []
    for token_1, token_2 in zip(tokens_1, tokens_2):
        equal_list.append(token_1 == token_2)

    if not all(equal_list):
        for token_1, token_2, equal in zip(tokens_1, tokens_2, equal_list):
            print(f"{token_1} == {token_2}: {equal}")

        assert False, "Token sequences are not equal."

    if len(tokens_1) != len(tokens_2):
        # Pad the shorter one with empty tokens.
        if len(tokens_1) < len(tokens_2):
            tokens_1 += ["?"] * (len(tokens_2) - len(tokens_1))
        else:
            tokens_2 += ["?"] * (len(tokens_1) - len(tokens_2))
        for token_1, token_2 in zip(tokens_1, tokens_2):
            print(f"{token_1} - {token_2}")
        assert False, "Token sequences are not equal."
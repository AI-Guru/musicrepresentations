import sys
sys.path.append("..")
from musicrepresentations.converter import (
    SongDataToNoteSequenceConverter,
    SongDataToTokensConverter,
    TokensToSongDataConverter,
    LlmDataToTokensConverter
)

# Get the path of this file.
import os
path = os.path.dirname(os.path.realpath(__file__))
llmdata_path = os.path.join(path, "data", "llm_sample.txt")
assert os.path.exists(llmdata_path), f"Invalid path: {llmdata_path}"
tokens_path = os.path.join(path, "data", "tokens_sample.txt")
assert os.path.exists(tokens_path), f"Invalid path: {tokens_path}"



def test_llmdata_to_tokens():
    llmdata = open(llmdata_path).read()
    print(llmdata)
    tokens = LlmDataToTokensConverter.convert(llmdata)
    print(tokens)
    songdata = TokensToSongDataConverter.convert(tokens)
    print(songdata)


def test_tokens_to_songdata():
    tokens = open(tokens_path).read()
    print(tokens)
    songdata = TokensToSongDataConverter.convert(tokens)
    print(songdata)

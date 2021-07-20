from typing import Any

from infiniteremixer.utils.io import load_from_pickle


class TempoExtractor:
    def __init__(self) -> None:
        pass

    def extract(self, path: str, song: str) -> Any:
        """Load the tempo extracted from the drums

        :return: Tempo of the song
        """
        tempo_dict = load_from_pickle(path)
        tempo = tempo_dict.get(song)
        return tempo

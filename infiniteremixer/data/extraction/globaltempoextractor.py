from infiniteremixer.utils.io import load_from_pickle

class TempoExtractor:

    def __init__(self, path):
        self.path = path

    def extract(self, song):
        """Load the tempo extracted from the drums

        :return: Tempo of the song
        """
        tempo_dict = load_from_pickle(self.path)
        tempo = tempo_dict.get(song)
        return tempo
        

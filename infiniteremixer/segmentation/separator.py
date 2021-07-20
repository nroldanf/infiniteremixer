import math
import os

import numpy as np
from spleeter.separator import Separator

from infiniteremixer.utils.io import load, write_wav


class SeparatorChunks:
    """Separate a track into 4 different sources and save the
    corresponding signals as audio files in different folders.

    The separator first divide in chunks that fit into RAM memory and Concatenate
    the results of prediction to an array.
    """

    def __init__(self, sample_rate, max_size):
        # Define the model
        self.separator = Separator("spleeter:4stems")
        self.max_size = max_size  # Maximum size of array (Equivalent 10_000_000 of 80M for a 2 channel audio).
        self.sample_rate = sample_rate
        self._audio_format = "wav"
        self.audio_array_length = None

    def create_and_save_sources(self, dir, save_dir):
        for root, _, files in os.walk(dir):
            for file in files:
                if file[-3:] in ["mp3", "wav"]:
                    self._separate(file, dir, save_dir)

    def _separate(self, file, root, save_dir):
        file_path = os.path.join(root, file)
        # Load the audio
        y = load(file_path, self.sample_rate, False)
        self.audio_array_length = y.shape[1]
        # Separate the audio
        if not self._is_file_too_big():
            other, drums = self._separate_full_file(y)
        else:
            other, drums = self._separate_by_chunks(y)
        # Generate the save path and save the audio
        audio_path_other = self._generate_save_path(file, save_dir, "other")
        audio_path_drums = self._generate_save_path(file, save_dir, "drums")
        write_wav(audio_path_other, other.T, self.sample_rate)
        write_wav(audio_path_drums, drums.T, self.sample_rate)
        # sf.write(save_path_other, other.T, self.sample_rate, subtype="PCM_24")
        # sf.write(save_path_drums, drums.T, self.sample_rate, subtype="PCM_24")

    def _generate_save_path(self, file, save_dir, source):
        file_name = f"{file}_{source}.{self._audio_format}"
        folder_path = self._create_save_path(file, save_dir)
        audio_path = os.path.join(folder_path, file_name)
        return audio_path

    def _create_save_path(self, file, save_dir):
        folder_path = os.path.join(save_dir, file)
        try:
            os.mkdir(folder_path)
        except OSError:
            print(f"{folder_path} already exists.")
        return folder_path

    # def _write_wav(self, file, save_root, save_dir, signal):
    #     # Save the separated files
    #     write_wav(save_dir, signal, self.sample_rate)

    def _is_file_too_big(self):
        return self.audio_array_length > self.max_size

    def _separate_full_file(self, stereo):
        # Get the different sources
        prediction = self.separator.separate(stereo.T)
        other, drums = prediction["other"], prediction["drums"]
        return other, drums

    def _separate_by_chunks(self, stereo):
        # Establish the number of chunks
        n_chunks = math.ceil(self.audio_array_length / self.max_size)
        # Initialize variables
        start_idx = 0
        end_idx = self.max_size
        other, drums = [], []
        for i in range(n_chunks):
            # Get sources for the chunk
            prediction = self.separator.separate(stereo[:, start_idx:end_idx].T)
            # Concatenate chunk predictions (sources) of interest
            other.append(prediction["other"].T)
            drums.append(prediction["drums"].T)

            start_idx = end_idx + 1

            # Frontier handling
            if (stereo.shape[1] - end_idx) <= self.max_size:
                end_idx = stereo.shape[1]
            else:
                end_idx += self.max_size + 1

        # Concatenate
        other = np.column_stack(other)
        drums = np.column_stack(drums)

        return other, drums


if __name__ == "__main__":
    sample_rate = 22050
    max_size = 6_000_000

    # os.mkdir("/app/results/splitted/tes1")
    separator = SeparatorChunks(sample_rate, max_size)
    separator.create_and_save_sources("/app/results/audios/", "/app/results/splitted")

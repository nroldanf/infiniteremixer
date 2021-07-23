import os

from infiniteremixer.segmentation.beattracker import estimate_beats_and_tempo
from infiniteremixer.segmentation.trackcutter import cut
from infiniteremixer.utils.io import load, save_to_pickle, write_wav


class SegmentExtractor:
    """SegmentExtractor is responsible to divide songs into beats and save
    the corresponding signals as audio files.
    """

    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self._audio_format = "wav"
        # self._tempo = {}

    # def create_and_save_segments(self, dir, audios_save_dir, data_save_dir):
    #     """Performs the following steps for each audio file in a
    #     directory:
    #         1- load audio file
    #         2- extract beat locations
    #         3- segment signal into as many chunks as beats we have
    #         4- save audio segments to wav

    #     :param dir: (str) Directory containing audio files to be preprocessed
    #     :param save_dir: (str) Directory where to save segments
    #     """
    #     for root, dirs, _ in os.walk(dir):
    #         for dir in dirs:
    #             audio_folder = os.path.join(root, dir)
    #             self._create_and_save_segments_for_file(
    #                 audio_folder, dir, audios_save_dir
    #             )
    #     # Save tempo
    #     self._create_save_path("", data_save_dir)
    #     dataset_path = self._save_data(data_save_dir, self._tempo, "tempo")
    #     print(f"Saved dataset to {dataset_path}")

    # def _create_and_save_segments_for_file(self, folder, root, save_dir):
    #     file_names = os.listdir(folder)
    #     file_paths = [
    #         os.path.join(folder, file_name) for file_name in os.listdir(folder)
    #     ]
    #     # Load both sources
    #     signal_drums = load(file_paths[0], self.sample_rate)
    #     signal_other = load(file_paths[1], self.sample_rate)
    #     # Estimate tempo from drums sources
    #     beat_events, tempo = estimate_beats_and_tempo(signal_drums, self.sample_rate)
    #     tempo_key = file_names[1].split("/")[-1]
    #     # print()
    #     # print("tempo key: ", tempo_key)
    #     # print()
    #     # self._tempo[tempo_key] = tempo
    #     # # Segment both based on beat events of drums source
    #     segments_drums = cut(signal_drums, beat_events)
    #     segments_other = cut(signal_other, beat_events)
    #     # Create folder for each source (drums and other)
    #     drums_path = self._create_save_path("drums", save_dir)
    #     other_path = self._create_save_path("other", save_dir)
    #     # Save the beats in different folders
    #     self._write_segments_to_wav(file_names[0], drums_path, segments_drums)
    #     self._write_segments_to_wav(file_names[1], other_path, segments_other)
    #     # Save the tempo file

    def create_and_save_segments(self, dir, save_dir):
        """Performs the following steps for each audio file in a
        directory:
            1- load audio file
            2- extract beat locations
            3- segment signal into as many chunks as beats we have
            4- save audio segments to wav
        :param dir: (str) Directory containing audio files to be preprocessed
        :param save_dir: (str) Directory where to save segments
        """
        for root, _, files in os.walk(dir):
            for file in files:
                if file.endswith("wav") or file.endswith("mp3"):
                    self._create_and_save_segments_for_file(file, dir, save_dir)

    def _create_and_save_segments_for_file(self, file, root, save_dir):
        file_path = os.path.join(root, file)
        signal = load(file_path, self.sample_rate)
        beat_events, _ = estimate_beats_and_tempo(signal, self.sample_rate)
        segments = cut(signal, beat_events)
        self._write_segments_to_wav(file, save_dir, segments)
        print(f"Beats saved for {file_path}")

    def _write_segments_to_wav(self, file, save_dir, segments):
        for i, segment in enumerate(segments):
            save_path = self._generate_save_path(file, save_dir, i)
            write_wav(save_path, segment, self.sample_rate)

    def _generate_save_path(self, file, save_dir, num_segment):
        file_name = f"{file}_{num_segment}.{self._audio_format}"
        save_path = os.path.join(save_dir, file_name)
        return save_path

    def _create_save_path(self, file, save_dir):
        folder_path = os.path.join(save_dir, file)
        try:
            os.mkdir(folder_path)
        except OSError:
            print(f"{folder_path} already exists.")
        return folder_path

    def _save_data(self, save_dir, data, data_type):
        save_path = os.path.join(save_dir, f"{data_type}.pkl")
        save_to_pickle(save_path, data)
        return save_path


if __name__ == "__main__":
    dir = "/app/results/splitted"
    save_dir = "/app/results/segmented"
    sr = 22050
    segment_extractor = SegmentExtractor(sr)
    segment_extractor.create_and_save_segments(dir, save_dir, "/app/results/dataset")

import os
from typing import List, Union

import numpy as np

from infiniteremixer.utils.io import save_to_pickle


class DatasetPipeline:
    """DatasetPipeline is an end-to-end pipeline responsible to generate
    and store embeddings for a group of audio files. It provides a pipeline
    that's responsible for:
        1- extracting features from audio files
        2- performing statistical aggregation on the features to make
           embeddings time independent
        3- merging multiple feature types for each track
        5- creating mappings and dataset from merged features
        6- storing the mappings and dataset to disk
    """

    def __init__(self) -> None:
        self.batch_extractor = None
        self.multi_track_batch_aggregator = None
        self.feature_merger = None
        self.global_tempo_extractor = None
        self.data_preparer = None

    def process(self, dir: str, save_dir: str, tempo_dir: str) -> None:
        """Generate embeddings for all audio files in a directory and
        store relative array dataset and mappings.

        :param dir: (str) Path to directory with audio files
        :param save_dir: (str) Path to directory where to save mappings and
            dataset
        """
        tracks_features = self.batch_extractor.extract(dir)
        # print(tracks_features)
        print("Extracted features")

        print()

        tracks_aggregations = self.multi_track_batch_aggregator.aggregate(
            tracks_features
        )
        # print(tracks_aggregations)
        print("Performed statistical aggregation of features")

        print()

        tracks_merged_features = self.feature_merger.merge(tracks_aggregations)
        # print(tracks_merged_features) # dict (key: np.array 1 x n_features)
        print("Merged multiple features")

        # track_merged_features = self.global_tempo_extractor.concatenate()

        mapping, dataset = self.data_preparer.prepare_mapping_and_dataset(
            tracks_merged_features
        )
        print("Mapping")
        print(mapping)

        song_name = [self._get_filename(path) for path in mapping][0]

        tempo = self.global_tempo_extractor.extract(tempo_dir, song_name)
        print("TEMPO ", tempo)

        print("Prepared mapping and dataset")
        mapping_path = self._save_data(save_dir, mapping, "mapping")
        print(f"Saved mapping to {mapping_path}")
        dataset_path = self._save_data(save_dir, dataset, "dataset")
        print(f"Saved dataset to {dataset_path}")

    def _save_data(
        self, save_dir: str, data: Union[List[str], np.ndarray], data_type: str
    ) -> str:
        save_path = os.path.join(save_dir, f"{data_type}.pkl")
        save_to_pickle(save_path, data)
        return save_path

    def _get_filename(self, path: str) -> str:
        parts = path.split("/")[-1].split(".")
        filename = parts[0] + "." + parts[1] + "." + parts[2][0:3]
        return filename

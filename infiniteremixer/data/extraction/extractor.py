from abc import ABC, abstractmethod

import numpy as np


class Extractor(ABC):
    """Interface for feature extractors."""

    def __init__(self, feature_name: str) -> None:
        self.feature_name = feature_name

    @abstractmethod
    def extract(self, signal: np.ndarray, sample_rate: int) -> None:
        pass

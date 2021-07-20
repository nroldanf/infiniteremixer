from abc import ABC, abstractmethod

import numpy as np


class Aggregator(ABC):
    """Interface for a concrete statistical aggregator."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def aggregate(self, array: np.ndarray) -> np.ndarray:
        pass

from abc import ABC, abstractmethod

import numpy as np

from infiniteremixer.data.aggregation.aggregator import Aggregator


class BatchAggregator(ABC):
    """BatchAggregator is an abstract class that provides an interface
    to apply multiple statistical aggregation on 2d numpy arrays.
    """

    def __init__(self) -> None:
        self.aggregators = []

    def add_aggregator(self, aggregator: Aggregator) -> None:
        """Add an aggregator function to the aggregators.

        :param aggregator: (Aggregator) Concrete Aggregator
        """
        self.aggregators.append(aggregator)

    @abstractmethod
    def aggregate(self, array: np.ndarray) -> np.ndarray:
        pass

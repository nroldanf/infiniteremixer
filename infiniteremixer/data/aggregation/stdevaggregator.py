import numpy as np

from infiniteremixer.data.aggregation.aggregator import Aggregator


class StdDeviationAggregator(Aggregator):
    """StdDeviationAggregator is responsible for aggregating a array using
    standard deviation across a specified axis.
    """

    def __init__(self, aggregation_axis: int) -> None:
        super().__init__("std_deviation")
        self.aggregation_axis = aggregation_axis

    def aggregate(self, array: np.ndarray) -> np.ndarray:
        """Aggregate array using std deviation across 1 axis.

        :param array: (np.ndarray)

        :return: (np.ndarray) Aggregated array
        """
        return np.std(array, axis=self.aggregation_axis)

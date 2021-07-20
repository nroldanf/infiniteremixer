from typing import List

import numpy as np


def concatenate_arrays(arrays: List[np.ndarray]) -> np.ndarray:
    """Concatenate list of arrays.

    :param arrays (list of np.ndarray)

    :return: (np.ndarray) Concatenated array
    """
    return np.hstack(arrays)

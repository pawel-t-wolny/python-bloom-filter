"""
This module implements a Segment class, used as part of a Bloom filter.
"""

from math import ceil, log, log2
from typing import Optional

from bitarray import bitarray
from mmh3 import hash as mmh3_hash


class Segment:
    """
    Class representing a single segment of a Bloom filter. A regular Bloom filter consists
    of only a single segment while a scalable Bloom filter consists of multiple segments.
    """

    def __init__(
        self,
        max_error: float,
        max_elements: Optional[int] = None,
    ):
        self.max_error = max_error
        if max_elements:
            # Regular bloom filter mode
            self.max_elements = max_elements
            self._calculate_segment_params()
            self._array = bitarray(self._array_size)

    def add(self, item) -> None:
        """
        Add an item to the segment.
        :param item: The item to be added.
        """
        slice_index = 0
        for s in range(0, self._num_of_slices):
            index = mmh3_hash(item, s, False) % self._slice_size
            self._array[slice_index + index] = 1
            slice_index += self._slice_size

    def contains(self, item) -> bool:
        """
        Check if the segment contains the given item.
        :param item: The item to be checked.
        :return: True if the filter might contain the item and False if it does not contain the
        item.
        """
        slice_index = 0
        for s in range(0, self._num_of_slices):
            index = mmh3_hash(item, s, False) % self._slice_size
            if not self._array[slice_index + index]:
                return False
            slice_index += self._slice_size
        return True

    @property
    def fill_ratio(self) -> float:
        """Returns the average fill ratio for the segment"""
        return self._array.count() / len(self._array)

    def _calculate_segment_params(self):
        num_of_slices = ceil(log2(1 / self.max_error))
        array_size = ceil(self.max_elements * abs(log(self.max_error)) / pow(log(2), 2))
        # The step below ensures that the filter size is divisible by the number of slices
        array_size += num_of_slices - array_size % num_of_slices
        slice_size = array_size // num_of_slices

        self._num_of_slices = num_of_slices
        self._array_size = array_size
        self._slice_size = slice_size

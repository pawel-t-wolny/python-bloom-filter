"""
This module implements a Segment class, used as part of a Bloom filter.
"""

from math import ceil, log, log2
from typing import Optional

from bitarray import bitarray
from mmh3 import hash as mmh3_hash

# Parameters for the scalable mode
_R_PARAM = 0.9
_S_PARAM = 4
_INIT_M_PARAM = 128


class SegmentFullError(Exception):
    """Custom exception for when the filter segment has exceeded its capacity."""

    def __init__(self, message: str):
        super().__init__(message)


class Segment:
    """
    Class representing a single segment of a Bloom filter. A regular Bloom filter consists
    of only a single segment while a scalable Bloom filter consists of multiple segments.
    """

    def __init__(
        self,
        *,
        max_filter_error: Optional[float] = None,
        max_elements: Optional[int] = None,
        previous_segment: Optional["Segment"] = None,
    ):
        if max_elements is not None:
            if max_filter_error is None:
                raise ValueError(
                    "Argument max_filter_error cannot be None if max_elements is not None"
                )
            # Regular bloom filter mode
            self.max_error = max_filter_error
            self.max_elements = max_elements
            self.__calculate_regular_segment_params()
        else:
            # Scalable bloom filter mode
            if previous_segment is None and max_filter_error is None:
                raise ValueError(
                    "Either max_filter_error or previous_segment must be provided"
                )
            self.__calculate_scalable_segment_params(previous_segment, max_filter_error)

        self._array = bitarray(self._array_size)

    def add(self, item) -> None:
        """
        Add an item to the segment.
        :param item: The item to be added.
        """
        if self._fill_ratio >= 0.5:
            raise SegmentFullError("The segment is full")
        slice_index = 0
        for s in range(0, self._num_of_slices):
            index = mmh3_hash(item, s, False) % self.slice_size
            self._array[slice_index + index] = 1
            slice_index += self.slice_size

    def contains(self, item) -> bool:
        """
        Check if the segment contains the given item.
        :param item: The item to be checked.
        :return: True if the filter might contain the item and False if it does not contain the
        item.
        """
        slice_index = 0
        for s in range(0, self._num_of_slices):
            index = mmh3_hash(item, s, False) % self.slice_size
            if not self._array[slice_index + index]:
                return False
            slice_index += self.slice_size
        return True

    @property
    def _fill_ratio(self) -> float:
        """Returns the average fill ratio for the segment"""
        return self._array.count() / len(self._array)

    def __calculate_regular_segment_params(self):
        num_of_slices = ceil(log2(1 / self.max_error))
        array_size = ceil(self.max_elements * abs(log(self.max_error)) / pow(log(2), 2))
        # The step below ensures that the filter size is divisible by the number of slices
        array_size += num_of_slices - array_size % num_of_slices
        slice_size = array_size // num_of_slices

        self._num_of_slices = num_of_slices
        self._array_size = array_size
        self.slice_size = slice_size

    def __calculate_scalable_segment_params(
        self,
        previous_segment: Optional["Segment"] = None,
        max_filter_error: Optional[float] = None,
    ) -> None:
        if not previous_segment and max_filter_error is None:
            raise ValueError(
                "Arguments previous_segment and max_filter_error cannot both be None"
            )

        if not previous_segment:
            # Computing the max_error for the segment based on the maximum false positive
            # error for the entire filter
            self.max_error = max_filter_error * (1 - _R_PARAM)
            self.slice_size = _INIT_M_PARAM

        else:
            # Computing the next max_error in the sequence
            self.max_error = previous_segment.max_error * _R_PARAM
            self.slice_size = previous_segment.slice_size * _S_PARAM

        self._num_of_slices = ceil(log2(1 / self.max_error))
        self._array_size = self._num_of_slices * self.slice_size

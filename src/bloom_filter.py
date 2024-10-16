from typing import Optional
from math import log2, log, pow, ceil

from mmh3 import hash
from bitarray import bitarray


class BloomFilter(object):

    def __init__(
            self,
            max_error: float,
            max_elements: Optional[int] = None,
    ) -> None:

        if not 0 < max_error < 1:
            raise ValueError("Argument max_error has to have a value between 0 and 1")
        self.max_error = max_error

        if max_elements is None:
            # Scalable bloom filter mode
            raise NotImplementedError
        else:
            # Regular bloom filter mode
            if not 0 < max_elements:
                raise ValueError(
                    "Argument max_elements has to be a value greater than 0"
                )
            self.max_elements = max_elements
            self._calculate_filter_params()
            self._array = bitarray(self._filter_size)

    def _calculate_filter_params(self):
        num_of_slices = ceil(log2(1 / self.max_error))
        filter_size = ceil(
            self.max_elements * abs(log(self.max_error)) / pow(log(2), 2)
        )
        # The step below ensures that the filter size is divisible by the number of slices
        filter_size += num_of_slices - filter_size % num_of_slices
        slice_size = filter_size // num_of_slices

        self._num_of_slices = num_of_slices
        self._filter_size = filter_size
        self._slice_size = slice_size

    def add(self, item):
        slice_index = 0
        for s in range(0, self._num_of_slices):
            index = hash(item, s, False) % self._slice_size
            self._array[slice_index + index] = 1
            slice_index += self._slice_size

    def contains(self, item) -> bool:
        slice_index = 0
        for s in range(0, self._num_of_slices):
            index = hash(item, s, False) % self._slice_size
            if not self._array[slice_index + index]:
                return False
            slice_index += self._slice_size
        return True

from io import BytesIO
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
            self._k, m = self._calculate_filter_params()
            self.filter = bitarray(m)

    def _calculate_filter_params(self) -> tuple[int, int]:
        k = ceil(log2(1 / self.max_error))
        m = ceil(self.max_elements * abs(log(self.max_error)) / pow(log(2), 2))
        return k, m

    @staticmethod
    @NotImplemented
    def import_file() -> BytesIO:
        raise NotImplementedError

    @staticmethod
    @NotImplemented
    def export_file() -> BytesIO:
        raise NotImplementedError

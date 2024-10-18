"""
Implementation of regular and scalable bloom filters based on the theoretical description in the
paper by Almeida et al. (2007).

Authored by: Pawel Wolny
"""

from typing import Optional

from segment import Segment


class BloomFilter:
    """
    The general bloom filter class allowing both standard and scalable mode.
    """

    def __init__(
        self,
        max_error: float,
        max_elements: Optional[int] = None,
    ) -> None:

        if not 0 < max_error < 1:
            raise ValueError("Argument max_error has to have a value between 0 and 1")
        self.max_error = max_error

        if max_elements is None:
            self._arrays_and_counts = []

        else:
            # Regular bloom filter mode
            if not 0 < max_elements:
                raise ValueError(
                    "Argument max_elements has to be a value greater than 0"
                )
            self.max_elements = max_elements
            self._segment = Segment(max_error, max_elements)

    def add(self, item) -> None:
        """
        Add an item to the filter.
        :param item: The item to be added.
        """
        self._segment.add(item)

    def contains(self, item) -> bool:
        """
        Check if the filter contains the given item.
        :param item: The item to be checked.
        :return: True if the filter might contain the item and False if it does not contain the
        item.
        """
        return self._segment.contains(item)

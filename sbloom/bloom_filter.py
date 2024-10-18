"""
Implementation of regular and scalable bloom filters based on the theoretical description in the
paper by Almeida et al. (2007).

Authored by: Pawel Wolny
"""

from typing import Optional
from sbloom.segment import Segment, SegmentFullError


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

        if not max_elements:
            # Scalable bloom filter mode
            self.scalable = True
            initial_segment = Segment(max_filter_error=max_error)
            self._segments: list[Segment] = [initial_segment]

        else:
            # Regular bloom filter mode
            if not 0 < max_elements:
                raise ValueError(
                    "Argument max_elements has to be a value greater than 0"
                )
            self.scalable = False
            self.max_elements = max_elements
            self._segment = Segment(
                max_filter_error=max_error, max_elements=max_elements
            )

    def add(self, item) -> None:
        """
        Add an item to the filter.
        :param item: The item to be added.
        """
        if self.scalable:
            try:
                self._segments[-1].add(item)
            except SegmentFullError:
                new_segment = Segment(previous_segment=self._segments[-1])
                self._segments.append(new_segment)
                new_segment.add(item)
        else:
            self._segment.add(item)

    def contains(self, item) -> bool:
        """
        Check if the filter contains the given item.
        :param item: The item to be checked.
        :return: True if the filter might contain the item and False if it does not contain the
        item.
        """
        if self.scalable:
            return any(segment.contains(item) for segment in self._segments)
        return self._segment.contains(item)

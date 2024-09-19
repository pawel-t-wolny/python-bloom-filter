from typing import Optional


class BloomFilter(object):

    def __init__(
        self,
        max_error: float,
        input_space_size: int,
        scalable: bool = True,
        init_list: Optional[list[any]] = None,
    ) -> None:

        if not 0 < max_error < 1:
            raise ValueError("Argument max_error has to have a value between 0 and 1")
        self.max_error = max_error

        self.scalable = scalable

        if not scalable:
            if not 0 < input_space_size:
                raise ValueError(
                    "Argument input_space_size has to have a value greater than 0"
                )
            self.input_space_size = input_space_size

        if init_list:
            self.init_list = init_list

    @staticmethod
    @NotImplemented
    def read():
        pass

    @staticmethod
    @NotImplemented
    def write():
        pass

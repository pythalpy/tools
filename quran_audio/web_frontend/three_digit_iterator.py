class ThreeDigitFormatter:
    """
    An iterator that generates a range of three-digit numbers with leading zeros.
    """

    def __init__(self, start_value, end_value=None):
        """
        Initializes the iterator with a start and end value OR a list/tuple.
        
        Args:
            start_value (int | list | tuple): The starting number, 
                                              or a list/tuple [start, end].
            end_value (int, optional): The last number in the sequence. 
                                       If None, defaults to start_value.
        """
        # Handle list/tuple input
        if isinstance(start_value, (list, tuple)):
            if len(start_value) == 1:
                start_value, end_value = start_value[0], start_value[0]
            elif len(start_value) == 2:
                start_value, end_value = start_value
            else:
                raise ValueError("List/tuple must have 1 or 2 elements")

        self.current_value = start_value - 1
        self.end_value = end_value if end_value is not None else start_value

        if self.current_value >= self.end_value:
            raise ValueError("Start value cannot be greater than or equal to the end value.")

    def __iter__(self):
        return self

    def __next__(self):
        self.current_value += 1
        if self.current_value > self.end_value:
            raise StopIteration
        return f"{self.current_value:03d}"

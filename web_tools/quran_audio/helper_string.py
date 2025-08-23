class ThreeDigitFormatter:
    """
    An iterator that generates a range of three-digit numbers with leading zeros.
    """
    def __init__(self, start_value, end_value=None):
        """
        Initializes the iterator with a start and end value.
        If no end_value is provided, it iterates only for the single start_value.
        
        Args:
            start_value (int): The starting number for the sequence.
            end_value (int, optional): The last number in the sequence. 
                                       If None, the sequence contains only start_value.
        """
        self.current_value = start_value - 1
        self.end_value = end_value if end_value is not None else start_value

        if self.current_value >= self.end_value:
            raise ValueError("Start value cannot be greater than or equal to the end value.")
    
    def __iter__(self):
        """
        Returns the iterator object itself.
        """
        return self
    
    def __next__(self):
        """
        Generates the next formatted three-digit number in the sequence.
        """
        self.current_value += 1
        if self.current_value > self.end_value:
            raise StopIteration
        
        return f"{self.current_value:03d}"
    
def range_padder(range_start, range_end):
    """
    Produces a range of surah numbers padded with leading zeros
    e.g.  1, 4 --> 001, 002, 003, 004
    """
    return ThreeDigitFormatter(range_start, range_end)
#specialNumbers.py

def vampire_number(id):
        """
        Determines if a given number is a vampire number.

        Args:
            id (int): The number to be checked.

        Returns:
            bool: True if the number is a vampire number, False otherwise.
        """
        
        if id < 1260:  # The smallest vampire number is 1260
            return False
    
        str_id = str(id)
        len_id = len(str_id)
    
        if len_id % 2 != 0:  # Must have an even number of digits
            return False
    
        half_len = len_id // 2
    
        # Iterate over potential fangs
        for x in range(10**(half_len - 1), 10**half_len):
            if id % x == 0:
                y = id // x
                # Ensure y has the correct number of digits
                if 10**(half_len - 1) <= y < 10**half_len:
                    # Check if neither x nor y end in 0
                    if not (x % 10 == 0 and y % 10 == 0):
                        # Check if the digits of x and y match the digits of n
                        if sorted(str(x) + str(y)) == sorted(str_id):
                            return True
    
        return False

import math
def is_perfect_number(n: int) -> bool:
    """
    Determines if a given number is a perfect number.
    
    A perfect number is a positive integer that is equal to the sum of its proper divisors, excluding the number itself.
    
    Args:
        n (int): The number to check if it is a perfect number.
        
    Returns:
        bool: True if the number is a perfect number, False otherwise.
    """
    #this version is way faster by using math.sqrt
    if n <= 1:
        return False
    
    sum_of_divisors = 1
    sqrt_n = int(math.sqrt(n))
    
    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            sum_of_divisors += i
            if i != n // i:
                sum_of_divisors += n // i
    
    return sum_of_divisors == n


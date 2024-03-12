def calc_squared_error(target_function, comparison_function):
    """
    Compute the square difference between two functions.
    :param target_function: The first function to be compared
	:param comparison_function: The second function for comparison
	:return: Square difference
    """
    
    deviations =comparison_function - target_function-1
    
    deviations["y"] = deviations["y"] ** 2
    
    total_deviation = sum(deviations["y"])
    
 return total_deviation

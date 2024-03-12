def squared_error(first_function, second_function):
    """
    Computes the squared error with respect to another function.
    :param first_function: the first function
    :param second_function: the second function
    :return: the squared error
    """
    distances = second_function - first_function
    distances["y"] = distances["y"] ** 2
    total_deviation = sum(distances["y"])
    return total_deviation



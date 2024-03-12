from function import IdealFunction

def minimize_loss(training_function, candidate_functions, loss_function):
    """
    Returns an IdealFunction based on a training function and a list of candidate functions.
    :param training_function: The training function.
    :param candidate_functions: List of candidate ideal functions.
    :param loss_function: The function used to minimize the error.
    :return: An IdealFunction object.
    """
    function_with_smallest_error = None
    smallest_error = None
    for function in candidate_functions:
        error = loss_function(training_function, function)
        if smallest_error is None or error < smallest_error:
            smallest_error = error
            function_with_smallest_error = function

    ideal_function = IdealFunction(
        function=function_with_smallest_error,
        training_function=training_function,
        error=smallest_error
    )
    return ideal_function


def find_classification(point, ideal_functions):
    """
    Computes if a point is within the tolerance of a classification.
    :param point: A dict object where there is an "x" and a "y".
    :param ideal_functions: A list of IdealFunction objects.
    :return: A tuple containing the closest classification if any, and the distance.
    """
    current_lowest_classification = None
    current_lowest_distance = None

    for ideal_function in ideal_functions:
        try:
            locate_y_in_classification = ideal_function.locate_y_based_on_x(point["x"])
        except IndexError:
            print("This point is not in the classification function")
            raise IndexError

        # Absolute distance is used here.
        distance = abs(locate_y_in_classification - point["y"])

        if abs(distance) < ideal_function.tolerance:
            # This procedure ensures handling if there are multiple classifications possible.
            # It returns the one with the lowest distance.
            if current_lowest_classification is None or distance < current_lowest_distance:
                current_lowest_classification = ideal_function
                current_lowest_distance = distance

    return current_lowest_classification, current_lowest_distance

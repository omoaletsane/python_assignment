from function import IdealFunction

def minimise_loss(training_function, list_of_candidate_functions, loss_function):
    """
    Produces an IdealFunction based on a training function and a list of candidate functions.
    :param training_function: the training function
    :param list_of_candidate_functions: list of candidate functions
    :param loss_function: the function used to minimize the error
    :return: an IdealFunction object
    """
    function_with_smallest_error = None
    smallest_error = None
    for function in list_of_candidate_functions:
        error = loss_function(training_function, function)
        if ((smallest_error == None) or error < smallest_error):
            smallest_error = error
            function_with_smallest_error = function

    ideal_function = IdealFunction(function=function_with_smallest_error, training_function=training_function,
                          error=smallest_error)
    return ideal_function


def find_classification(point, ideal_functions):
    """
    Determines if a point falls within the tolerance of a classification.
    :param point: a dictionary containing "x" and "y" coordinates
    :param ideal_functions: a list of IdealFunction objects
    :return: a tuple containing the closest classification if any, and the distance
    """
    current_lowest_classification = None
    current_lowest_distance = None

    for ideal_function in ideal_functions:
        try:
            locate_y_in_classification = ideal_function.locate_y_based_on_x(point["x"])
        except IndexError:
            print("This point is not in the classification function")
            raise IndexError

        # Here, absolute distance is used
        distance = abs(locate_y_in_classification - point["y"])

        if (abs(distance < ideal_function.tolerance)):
            # This procedure ensures handling for multiple possible classifications
            # It returns the one with the lowest distance
            if ((current_lowest_classification == None) or (distance < current_lowest_distance)):
                current_lowest_classification = ideal_function
                current_lowest_distance = distance

    return current_lowest_classification, current_lowest_distance

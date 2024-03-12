import math

from function import FunctionManager
from lossfunction import squared_error
from plotting import (plot_ideal_functions,
                      plot_points_with_their_ideal_function)
from regression import find_classification, minimise_loss
from utils import write_deviation_results_to_sqlite

# This constant represents the factor for the criterion, specific to the assignment
ACCEPTED_FACTOR = math.sqrt(2)

if __name__ == '__main__':
    # Specify paths for csv files
    ideal_path = "data/ideal.csv"
    train_path = "data/train.csv"

    # The FunctionManager accepts a path to a csv and parses Function objects from the data.
    # A Function stores X and Y points of a function. It utilizes Pandas for efficient data handling.
    candidate_ideal_function_manager = FunctionManager(path_of_csv=ideal_path)
    train_function_manager = FunctionManager(path_of_csv=train_path)

    # A FunctionManager uses the .to_sql function from Pandas
    # The suffix is added to conform to the requirement of the table structure
    train_function_manager.to_sql(file_name="output/training", suffix=" (training func)")
    candidate_ideal_function_manager.to_sql(file_name="output/ideal", suffix=" (ideal func)")

    # Recap:
    # Within train_function_manager, 4 functions are stored.
    # Within ideal_function_manager, 50 functions are stored.
    # In the next step, we can use this data to compute an IdealFunction.
    # An IdealFunction, among other things, stores the best-fitting function, the training data, and is able to compute the tolerance.
    # All we need to do now is iterate over all train_functions
    # Matching ideal functions are stored in a list.
    ideal_functions = []
    for train_function in train_function_manager:
        # minimise_loss is capable of computing the best-fitting function given the train function
        ideal_function = minimise_loss(training_function=train_function,
                                       list_of_candidate_functions=candidate_ideal_function_manager.functions,
                                       loss_function=squared_error)
        ideal_function.tolerance_factor = ACCEPTED_FACTOR
        ideal_functions.append(ideal_function)

    # We can use the classification to perform some plotting
    plot_ideal_functions(ideal_functions, "output/train_and_ideal")

    # Now it is time to analyze all points within the test data
    # The FunctionManager provides all the necessary tools to load a CSV, so it will be reused.
    # Instead of multiple Functions like before, it will now contain a single "Function" at location [0]
    # The benefit is that we can iterate over each point with the Function object
    test_path = "data/test.csv"
    test_function_manager = FunctionManager(path_of_csv=test_path)
    test_function = test_function_manager.functions[0]

    points_with_ideal_function = []
    for point in test_function:
        ideal_function, delta_y = find_classification(point=point, ideal_functions=ideal_functions)
        result = {"point": point, "classification": ideal_function, "delta_y": delta_y}
        points_with_ideal_function.append(result)

    # Recap: within points_with_ideal_functions a list of dictionaries is stored.
    # These dictionaries represent the classification result of each point.

    # We can plot all the points with the corresponding classification function
    plot_points_with_their_ideal_function(points_with_ideal_function, "output/point_and_ideal")

    # Finally, the dict object is used to write it to a SQLite database
    # In this method, a pure SQLAlchemy approach has been chosen with a MetaData object to avoid using SQL language directly
    write_deviation_results_to_sqlite(points_with_ideal_function)
    
    print("Following files were created:")
    print("training.db: Contains all training functions stored as a SQLite database")
    print("ideal.db: Contains all ideal functions stored as a SQLite database")
    print("mapping.db: Contains the results of the point test where the ideal function and its delta are computed")
    print("train_and_ideal.html: View the training data as scatter and the best-fitting ideal function as a curve")
    print("points_and_ideal.html: View for those points with a matching ideal function the distance between them in a figure")
    print("Script completed successfully")



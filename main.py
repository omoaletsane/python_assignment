import math
from function import FunctionManager
from lossfunction import calc_squared_error
from plotting import (plot_ideal_functions,
                      plot_points_with_their_ideal_function)
from regression import find_classification, minimise_loss
from utils import write_deviation_results_to_sqlite

# Constant factor for the criterion, specific to the assignment
ACCEPTED_FACTOR = math.sqrt(2)

if __name__ == '__main__':
    # Paths for csv files
    ideal_path = "data/ideal.csv"
    train_path = "data/train.csv"

    # Initialize FunctionManagers to parse Function objects from csv data
    candidate_ideal_function_manager = FunctionManager(path_of_csv=ideal_path)
    train_function_manager = FunctionManager(path_of_csv=train_path)

    # Store Function objects in SQLite databases
    train_function_manager.to_sql(file_name="output/training", suffix=" (training func)")
    candidate_ideal_function_manager.to_sql(file_name="output/ideal", suffix=" (ideal func)")

    # Compute IdealFunction for each training function
    ideal_functions = []
    for train_function in train_function_manager:
        ideal_function = minimise_loss(training_function=train_function,
                                       list_of_candidate_functions=candidate_ideal_function_manager.functions,
                                       loss_function=squared_error)
        ideal_function.tolerance_factor = ACCEPTED_FACTOR
        ideal_functions.append(ideal_function)

    # Plot ideal functions
    plot_ideal_functions(ideal_functions, "output/train_and_ideal")

    # Process test data
    test_path = "data/test.csv"
    test_function_manager = FunctionManager(path_of_csv=test_path)
    test_function = test_function_manager.functions[0]

    points_with_ideal_function = []
    for point in test_function:
        ideal_function, delta_y = find_classification(point=point, ideal_functions=ideal_functions)
        result = {"point": point, "classification": ideal_function, "delta_y": delta_y}
        points_with_ideal_function.append(result)

    # Plot points with corresponding ideal function
    plot_points_with_their_ideal_function(points_with_ideal_function, "output/point_and_ideal")

    # Write results to SQLite
    write_deviation_results_to_sqlite(points_with_ideal_function)
    
    # Output created files and completion message
    print("Files created:")
    print("training.db: SQLite database containing all training functions")
    print("ideal.db: SQLite database containing all ideal functions")
    print("mapping.db: Results of point test including ideal function and delta")
    print("train_and_ideal.html: Visualization of training data and best fitting ideal function")
    print("points_and_ideal.html: Visualization showing distance between points and their ideal function")
    print("Script completed successfully")
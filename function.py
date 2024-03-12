import pandas as pd
from sqlalchemy import create_engine

class FunctionManager:
    def __init__(self, csv_path):
        """
        A list of strings that represents functions is created by parsing a CSV file stored locally. By iterating through an object, we are able to access a function.
        The class of Functions can also be obtained by noting the property .functions.
        The structure of the CSV must be such that there is: first column for x-values and additional columns for y-values.
     
        Args:
            csv_path (str): Local path to the CSV.
        """
        self._functions = []

        # Reading the CSV using the Pandas module and converting it into a DataFrame
        try:
            self._function_data = pd.read_csv(csv_path)
        except FileNotFoundError:
            print("Error while reading file {}".format(csv_path))
            raise

        # Storing x-values to later feed into each Function
        x_values = self._function_data["x"]

        # Iterating over each column within the Pandas DataFrame to create a new Function object from the data
        for column_name, column_data in self._function_data.items():
            if "x" in column_name:
                continue
            # Concatenating x and y columns to create a subset DataFrame for each Function
            subset = pd.concat([x_values, column_data], axis=1)
            function = Function.from_dataframe(column_name, subset)
            self._functions.append(function)

    def to_sql(self, db_name, suffix):
        """
        Use the Pandas method to_sql() to save the information in a local SQLite database.
        It is overwritten if the file already exists.
        
        Args:
            db_name (str): The name of the database.
            suffix (str): Suffix required for headers to fit into an assignment.
        """
        # Creating an SQLAlchemy engine to handle database creation if it does not exist
        engine = create_engine('sqlite:///{}.db'.format(db_name), echo=False)

        # Modifying column names to comply with assignment requirements
        copy_of_function_data = self._function_data.copy()
        copy_of_function_data.columns = [name.capitalize() + suffix for name in copy_of_function_data.columns]
        copy_of_function_data.set_index(copy_of_function_data.columns[0], inplace=True)

        copy_of_function_data.to_sql(
            db_name,
            engine,
            if_exists="replace",
            index=True,
        )

    @property
    def functions(self):
        """
        It fetches all functions in a list. Alternatively, one can loop over the object directly.
        
        Returns:
            list: it contains functions
        """
        return self._functions

    def __iter__(self):
        """
        Makes the object iterable.
        """
        return FunctionManagerIterator(self)

    def __repr__(self):
        return "Contains {} functions.".format(len(self.functions))


class FunctionManagerIterator:
    def __init__(self, function_manager):
        """
        This function is used for iterating through a FunctionManager object
        
        Args:
            function_manager (FunctionManager): The FunctionManager object that should be iterated upon
        """
        self._index = 0
        self._function_manager = function_manager

    def __next__(self):
        """
        The returns is an object of a function as it loops through the list of functions.
        
        Returns:
            Function: A function object.
        """
        if self._index < len(self._function_manager.functions):
            value_requested = self._function_manager.functions[self._index]
            self._index += 1
            return value_requested
        raise StopIteration


class Function:
    def __init__(self, name):
        """
        A dataframe in pandas that holds X and Y values for a certain function.
        
        Args:
            name (str): The name of the function.
        """
        self._name = name
        self.dataframe = pd.DataFrame()

    def locate_y_based_on_x(self, x):
        """
        Given the X-Value, retrieves its corresponding Y-Value. 
        
        Args:
            x (float): The X-Value.
            
        Returns:
            float: The Y-Value.
        """
        try:
            return self.dataframe.loc[self.dataframe["x"] == x, "y"].iloc[0]
        except IndexError:
            raise IndexError("Y-Value not found for the given X.")

    @property
    def name(self):
        """
        It returns the function’s name as a string type.
        
        Returns:
            str: The name of the function.
        """
        return self._name

    def __iter__(self):
        """
        Makes the object iterable.
        """
        return FunctionIterator(self)

    def __sub__(self, other):
        """
        It subtracts two functions and returns a new DataFrame.
        
        Args:
            other (Function): The function to subtract from this function.
            
        Returns:
            pd.DataFrame: A DataFrame representing the difference between the two functions.
        """
        diff = self.dataframe - other.dataframe
        return diff

    @classmethod
    def from_dataframe(cls, name, dataframe):
        """
        It creates a function from a DataFrame.
        
        Args:
            name (str): The name of the function.
            dataframe (pd.DataFrame): The DataFrame containing x and y values.
            
        Returns:
            Function: A Function object.
        """
        function = cls(name)
        function.dataframe = dataframe
        function.dataframe.columns = ["x", "y"]
        return function

    def __repr__(self):
        return "Function: {}".format(self.name)


class IdealFunction(Function):
    def __init__(self, function, training_function, error):
        """
        It stores the predicting function, training data, and the regression.
        
        Args:
            function (Function): The ideal function.
            training_function (Function): The training data the classifying data is based upon.
            error (float): The regression error.
        """
        super().__init__(function.name)
        self.dataframe = function.dataframe
        self.training_function = training_function
        self.error = error
        self._tolerance_value = 1
        self._tolerance = 1

    def _determine_largest_deviation(self, ideal_function, train_function):
        """
        It determines the largest deviation between two functions.
        
        Args:
            ideal_function (Function): The ideal function.
            train_function (Function): The training function.
            
        Returns:
            float: The largest deviation.
        """
        distances = train_function - ideal_function
        distances["y"] = distances["y"].abs()
        largest_deviation = max(distances["y"])
        return largest_deviation

    @property
    def tolerance(self):
        """
        The property describing the accepted tolerance towards the regression.
        
        Returns:
            float: The tolerance value.
        """
        self._tolerance = self.tolerance_factor * self.largest_deviation
        return self._tolerance

    @tolerance.setter
    def tolerance(self, value):
        self._tolerance = value

    @property
    def tolerance_factor(self):
        """
        The property to set the factor of the largest deviation to determine the tolerance.
        
        Returns:
            float: The tolerance factor.
        """
        return self._tolerance_value

    @tolerance_factor.setter
    def tolerance_factor(self, value):
        self._tolerance_value = value


from sqlalchemy import Column, Float, MetaData, String, Table, create_engine


def write_deviation_results_to_sqlite(result):
    """
    Writes results of a classification computation to an SQLite database.
    It adheres to the requirements specified in the assignment.
    :param result: a list containing a dictionary describing the result of a classification test
    """
    # In this function, we employ a native SQLAlchemy approach
    # Instead of using SQL syntax, MetaData is used to describe the table and its columns
    # SQLAlchemy utilizes this data structure to create the table
    engine = create_engine('sqlite:///{}.db'.format("output/mapping"), echo=False)
    metadata = MetaData()

    mapping = Table('mapping', metadata,
                    Column('X (test func)', Float, primary_key=False),
                    Column('Y (test func)', Float),
                    Column('Delta Y (test func)', Float),
                    Column('No. of ideal func', String(50))
                    )

    metadata.create_all(engine)

    # Rather than inserting values line by line (which is slow),
    # SQLAlchemy's .execute is utilized with a dictionary containing all the values
    # The creation of this dictionary involves a straightforward mapping between my internal data structures and
    # the structure required for the assignment

    execute_map = []
    for item in result:
        point = item["point"]
        classification = item["classification"]
        delta_y = item["delta_y"]

        # We need to check if there is a classification for a point at all, and if so, rename the function name accordingly
        classification_name = None
        if classification is not None:
            classification_name = classification.name.replace("y", "N")
        else:
            # If there is no classification, there is also no distance. In that case, a dash is written
            classification_name = "-"
            delta_y = -1

        execute_map.append(
            {"X (test func)": point["x"], "Y (test func)": point["y"], "Delta Y (test func)": delta_y,
             "No. of ideal func": classification_name})

    # using the Table object, the dictionary is used to insert the data
    i = mapping.insert().values(execute_map)
    with engine.connect() as connection:
        connection.execute(i.compile(connection))
        connection.commit()

    #i.execute(execute_map)
    
    
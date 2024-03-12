from sqlalchemy import Column, Float, MetaData, String, Table, create_engine


def write_deviation_results_to_sqlite(result):
​ ​ ​  """
​ ​ ​  Writes classification computation results​ tо​ a SQLite database.
​ ​ ​ ​ 
​ ​ ​  This function uses SQLAlchemy​ tо define the﻿ table structure and insert data.
​ ​ ​ ​ 
​ ​ ​  Args:
​ ​ ​ ​ ​ ​ ​  result (list):​ A list containing dictionaries describing the result​ оf​ a classification test.
​ ​ ​  """
​ ​ ​ ​ # Create​ a SQLite database engine
​ ​ ​  engine​ = create_engine('sqlite:///{}.db'.format("output/mapping"), echo=False)
​ ​ ​ ​ 
​ ​ ​ ​ # Define metadata​ tо describe the﻿ table and its columns
​ ​ ​  metadata​ = MetaData()
​ ​ ​ ​ 
​ ​ ​  mapping​ = Table('mapping', metadata,
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  Column('X﻿ (test func)', Float, primary_key=False),
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  Column('Y﻿ (test func)', Float),
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  Column('Delta​ Y﻿ (test func)', Float),
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  Column('No.​ оf﻿ ideal func', String(50))
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  )

​ ​ ​ ​ # Create the﻿ table​ іn the database
​ ​ ​  metadata.create_all(engine)

​ ​ ​ ​ # Construct​ a list​ оf dictionaries​ tо insert data into the table
​ ​ ​  execute_map​ = []
​ ​ ​  for item​ іn result:
​ ​ ​ ​ ​ ​ ​ ﻿ point​ = item["point"]
​ ​ ​ ​ ​ ​ ​  classification​ = item["classification"]
​ ​ ​ ​ ​ ​ ​  delta_y​ = item["delta_y"]

​ ​ ​ ​ ​ ​ ​ ​ #﻿ Check​ іf﻿ there​ іs​ a classification for​ a point
​ ​ ​ ​ ​ ​ ​  classification_name​ =﻿ None
​ ​ ​ ​ ​ ​ ​ ​ іf classification​ іs not None:
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ # Rename the function name​ tо comply​ іf﻿ there​ іs​ a classification
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  classification_name​ = classification.name.replace("y",﻿ "N")
​ ​ ​ ​ ​ ​ ​  else:
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ #​ If﻿ there​ іs​ nо classification, assign​ a﻿ dash
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  classification_name​ = "-"
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  delta_y​ = -1

​ ​ ​ ​ ​ ​ ​  execute_map.append(
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  {"X﻿ (test func)": point["x"],​ "Y﻿ (test func)": point["y"], "Delta​ Y﻿ (test func)": delta_y,
​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​  "No.​ оf﻿ ideal func": classification_name})

​ ​ ​ ​ # Insert data into the﻿ table﻿ using SQLAlchemy's﻿ Table object
​ ​ ​  insert_statement​ = mapping.insert().values(execute_map)
​ ​ ​  with engine.connect()​ as connection:
​ ​ ​ ​ ​ ​ ​  connection.execute(insert_statement.compile(connection))
​ ​ ​ ​ ​ ​ ​  connection.commit()

​ ​ ​ ​ # Alternative approach: Directly execute the insert statement
​ ​ ​ ​ # insert_statement.execute(execute_map)

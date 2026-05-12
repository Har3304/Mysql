import pandas as pd
import numpy as np
import mysql.connector

df = pd.read_json('index.json')
print(df.head())
columns = list(df.columns)             
print(df.select_dtypes(include=['object']).columns.tolist())
print(df.select_dtypes(include=['float']).columns.tolist())
print(df.select_dtypes(include=['integer']).columns.tolist())

for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, list)).all():
        df[col] = df[col].apply(lambda x: ', '.join(x))

try:
    connection = mysql.connector.connect(
        host = 'localhost',
        database = 'test_db',
        user = 'root',
        password = 'Reimagine@123'
    )
    if connection.is_connected():
        cursor = connection.cursor()
        print('Connected to mysql database.')

        column_definition = []
        for col in columns:
            if col in df.select_dtypes(include=['object']).columns.tolist():
                column_definition.append(f"{col} varchar(255)")
            elif col in df.select_dtypes(include=['integer']).columns.tolist():
                column_definition.append(f'{col} int')
            elif col in df.select_dtypes(include=['float']).columns.tolist():
                column_definition.append(f'{col} float')                
            elif col in df.select_dtypes(include=['float']).columns.tolist():
                column_definition.append(f'{col} int')
            else:
                pass
        check_query = f'''drop table if exists json_sql;'''
        cursor.execute(check_query)        
        create_query = f'''create table json_sql ({', '.join(column_definition)})'''
        print('Creating Table')
        print(create_query)
        cursor.execute(create_query)
        print('table created successfully!')

        place_holder = ', '.join(['%s'] * len(columns))

        column_names =', '.join([f"`{col}`" for col in columns])

        insert_query = f"""
        insert into json_sql ({column_names})
        values ({place_holder})"""

        print('\ninsert_query:\n')
        print(insert_query)

        for _, row in df.iterrows():
            values = tuple(value for value in row)
            cursor.execute(insert_query, values)

        connection.commit()
        print(f'\n {cursor.rowcount} rows inserted successfully!')


        cursor.execute('select * from json_sql')
        rows = cursor.fetchall()
        print('\nInserted Data:\n')
        for row in rows:
            print(row)
        cursor.close()
        connection.close()

        print('\nMYSQL is closed.')
except mysql.connector.Error as error:
    print("Errors: ", error)
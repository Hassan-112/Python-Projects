import sqlite3
import sys
import os
sys.path.append('../')  # Adds the parent directory to the sys.path


db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'your_database.db'))

def edit_table_data(table_name, column_name, new_value, condition_column, condition_value):
 
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
        
        update_query = f"UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?"
        cursor.execute(update_query, (new_value, condition_value))

        conn.commit()
        print(f"Data in {column_name} column of {table_name} updated successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
       
        conn.close()
def delete_record_by_id(table_name, record_id):

    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
      
        delete_query = f"DELETE FROM {table_name} WHERE id = ?"
        cursor.execute(delete_query, (record_id,))

        
        conn.commit()
        print(f"Record with ID {record_id} deleted from {table_name} successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
        conn.close()
def delete_all_records(table_name):
   
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
        
        if conn.in_transaction:
            conn.commit()

        
        delete_query = f"DELETE FROM {table_name}"
        cursor.execute(delete_query)

        conn.commit()
        print(f"All records from {table_name} deleted successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
        
        conn.close()


def delete_column_from_table(table_name, column_name):
 
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
      
        cursor.execute(f"PRAGMA table_info({table_name});")
        existing_columns = [column[1] for column in cursor.fetchall()]


        if column_name in existing_columns:
            
            new_table_query = f"CREATE TABLE {table_name}_new AS SELECT {', '.join(existing_columns)} FROM {table_name};"
            cursor.execute(new_table_query)

         
            drop_old_table_query = f"DROP TABLE {table_name};"
            cursor.execute(drop_old_table_query)

            
            rename_table_query = f"ALTER TABLE {table_name}_new RENAME TO {table_name};"
            cursor.execute(rename_table_query)

           
            conn.commit()
            print(f"Column '{column_name}' deleted from {table_name} successfully.")

        else:
            print(f"Column '{column_name}' does not exist in table '{table_name}'.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
   
        conn.close()

def drop_table(table_name):
  
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = cursor.fetchone()

        if result:
          
            cursor.execute(f"DROP TABLE {table_name}")
            print(f"Table '{table_name}' dropped successfully.")
        else:
            print(f"Table '{table_name}' does not exist.")

      
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
       
        conn.close()

def add_column_to_table(table_name, column_name):
       
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
      
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN '{column_name}' INT;")

            
        conn.commit()
        print(f"New column {column_name} added successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
            
        conn.close()


def create_new_table(table_name, columns_definition):
    """
    Create a new table in the database.

    Parameters:
    - table_name: Name of the new table.
    - columns_definition: A string containing the column definitions for the new table.

    Example of columns_definition:
    "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
    """
 
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
        
        create_table_query = f"CREATE TABLE {table_name} ({columns_definition});"
        cursor.execute(create_table_query)

       
        conn.commit()
        print(f"Table '{table_name}' created successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
        conn.close()
def delete_database(database_path):
    try:
        if os.path.exists(database_path):
            
            os.remove(database_path)
            print(f"Database '{database_path}' deleted successfully.")
        else:
            print(f"Database '{database_path}' does not exist.")

    except Exception as e:
        print(f"Error: {e}")

def edit_table_data(table_name, column_name, new_value, condition_column, condition_value):
 
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
        
        update_query = f"UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?"
        cursor.execute(update_query, (new_value, condition_value))

        conn.commit()
        print(f"Data in {column_name} column of {table_name} updated successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
       
        conn.close()










        
      
        conn.close()

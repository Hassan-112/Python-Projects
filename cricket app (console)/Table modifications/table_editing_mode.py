
import table_modifications as a
import sys
import set_password as pswd

tr = 0
while True:
    tr += 1

    input_pswd = input('Enter Password: ')

    if pswd.code.get_code() == input_pswd:
        print("""\n1: add column to table\n2: create_new__table\n3: delete_database\n4: delete_all_records_from_table
        \n5: delete_column\n6: delete_record_by_id\n7: delete_table\n8: edit_table\n""")

        choice = int(input('Enter your choice: '))
        if choice == 1:
            table = input('Enter table name: ')
            column = input('Enter column name: ')
            a.add_column_to_table(table,column)
            break
        if choice == 2:
            table = input('Enter table name: ')
            column = input('columns Definition: ')
            a.create_new_table(table,column)
            break
        if choice == 3:
            path = input('db path: ')
            a.delete_database(path)
            break
        if choice == 4:
            table = input('Enter table name: ')
            a.delete_all_records(table)
            break
        if choice == 5:
            table = input('Enter table name: ')
            column = input('Enter column name: ')
            a.delete_column_from_table(table, column)
            break
        if choice == 6:
            table = input('Enter table name: ')
            idd = input('Enter id: ')
            delete_record_by_id(table, idd)
            break
        if choice ==7:
            table = input('Enter table name: ')
            a.drop_table(table)
            break
        if choice ==8:
            table = input('Enter table name: ')
            column = input('Enter column name: ')
            new_value = input('New value: ')
            condition_column = input('condition_column: ')
            condition_value = input('condition_value: ')
        

            a.edit_table_data(table, column,new_value,condition_column,condition_value)
            break
            
            
            
            
    else:
        if tr == 3:
            print("You failed to enter the correct password!")
            break
        print("Password Wrong!")
        print("Try again!")

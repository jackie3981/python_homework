# Task 2
import os, csv, custom_module
from datetime import datetime

# Common function to convert a CSV file into a dictionary, with an option to convert it into tuples
def read_csv_as_dict(file_path, convert_to_tuple=False):
    data = {}
    rows = []

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, newline="") as file:
            csvfile = csv.reader(file)
            for i, row in enumerate(csvfile):
                if i == 0:
                    data["fields"] = row
                else:
                    if convert_to_tuple:
                        rows.append(tuple(row))
                    else:
                        rows.append(row)

        data["rows"] = rows
        return data

    except Exception as e:
        print(f"Error: {e}")
        return None

# Read employee data and store it in a dictionary.
def read_employees():
    file_path = "../csv/employees.csv"
    return read_csv_as_dict(file_path)

employees = read_employees()

# Task 3
# Retrieve the index of the column given, by default return the employee_id index.
def column_index(column_name="employee_id"):
    return employees["fields"].index(column_name)

employee_id_column = column_index()

# Task 4
# Retrieve the first name of an employee on the given row number.
def first_name(row_number):
     return employees["rows"][row_number-1][column_index("first_name")]

# Task 5
def employee_find(employee_id):
    rows = []
    employee_id_index = column_index("employee_id")
    if employee_id_index == -1:
        return rows

    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))

    return matches

# Task 6
def employee_find_2(employee_id):
    matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
    return matches

# Task 7
def sort_by_last_name():
    employees["rows"] = sorted(employees["rows"], key=lambda row: row[column_index("last_name")])
    return employees["rows"]

# Task 8
def employee_dict(row):
    row_dictionary = dict(zip(employees["fields"],row))
    del row_dictionary["employee_id"]
    return row_dictionary

# Task 9
def all_employees_dict():
    employee_dictionary = {}

    for row in employees["rows"]:
        emp_id = row[0]
        employee_dictionary[emp_id] = employee_dict(row)

    return employee_dictionary

# Task 10;
# This line was added for this exercise
os.environ["THISVALUE"] = "ABC"

def get_this_value():
    return os.getenv("THISVALUE")

# Task 11
def set_that_secret(secret):
    custom_module.set_secret(secret)

set_that_secret("pythonTest")

# Task 12
def read_minutes():
    file_path_minutes1 = "../csv/minutes1.csv"
    file_path_minutes2 = "../csv/minutes2.csv"

    local_minutes1 = read_csv_as_dict(file_path_minutes1, convert_to_tuple=True)
    local_minutes2 = read_csv_as_dict(file_path_minutes2, convert_to_tuple=True)

    return local_minutes1, local_minutes2

minutes1, minutes2 = read_minutes()

# Task 13
def create_minutes_set():
    rows1 = [tuple(row) for row in minutes1["rows"]]
    rows2 = [tuple(row) for row in minutes2["rows"]]

    local_minutes_set = set(rows1 + rows2)

    return local_minutes_set

minutes_set = create_minutes_set()

# Task 14
def create_minutes_list():
    local_minutes_list = list(
        map(
            lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")),
            minutes_set
        )
    )

    return local_minutes_list

minutes_list = create_minutes_list()

# Task 15
def write_sorted_list():
    sorted_list = sorted(minutes_list, key=lambda x: x[1])

    converted_list = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")),sorted_list))

    # Write the new list to CSV file
    output_file_path = "./minutes.csv"
    try:
        with open(output_file_path, mode="w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(minutes1["fields"])

            for row in converted_list:
                writer.writerow(row)
    except Exception as e:
        print(f"Error while writing to file: {e}")
        return []

    return converted_list

write_sorted_list()
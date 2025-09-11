import pandas as pd
import json
from dateutil.parser import parse, ParserError

# Task 1
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)

# making a copy from the original data
task1_with_salary = task1_data_frame.copy()

# adding the new column
task1_with_salary['Salary'] = [70000, 80000, 90000]
# making a copy from task1_with_salary
task1_older = task1_with_salary.copy()
# Adding 1 to Age
task1_older['Age'] =  task1_older['Age'] +1
# saving data into employees.csv, index= False, sep= ","
task1_older.to_csv("employees.csv", sep=",", index=False)

# Task 2
task2_employees = pd.read_csv("employees.csv", sep=",")

additional_employees = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]

with open("additional_employees.json", "w") as f:
    json.dump(additional_employees, f, indent=4)

json_employees = pd.read_json("additional_employees.json")

more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)

# Task 3
first_three = more_employees.head(3)
last_two = more_employees.tail(2)

employee_shape = more_employees.shape

more_employees.info()

# Task 4
dirty_data = pd.read_csv("dirty_data.csv", sep=",")

clean_data = dirty_data.copy()
clean_data = clean_data.drop_duplicates()

clean_data["Age"] = pd.to_numeric(clean_data["Age"], errors="coerce")
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"].replace("unknown", pd.NA), errors="coerce")

clean_data["Age"] = clean_data["Age"].fillna(clean_data["Age"].mean())
clean_data["Salary"] = clean_data["Salary"].fillna(clean_data["Salary"].median())

clean_data["Name"] = clean_data["Name"].str.strip().str.upper()
clean_data["Department"] = clean_data["Department"].str.strip().str.upper()

def try_parse_date(date_str):
    original_date = date_str
    cleaned = date_str.strip()

    # change separators to '/'
    cleaned = cleaned.replace('-', '/').replace('.', '/')

    # Optional: Remove multiple spaces
    cleaned = ' '.join(cleaned.split())

    try:
        # parsing with dateutil
        dt = parse(cleaned, fuzzy=True, dayfirst=True)

        # year out of range
        if dt.year < 1900 or dt.year > 2100:
            return f"Year out of range: '{original_date}'"

        return dt.strftime('%Y-%m-%d')

    except (ValueError, ParserError):
        return original_date

clean_data['Hire Date'] = [try_parse_date(hired_date) for hired_date in clean_data['Hire Date']]

# Final conversion to datetime
clean_data["Hire Date"] = pd.to_datetime(clean_data["Hire Date"], errors="coerce")


# Task 1
# print(task1_data_frame)
# print(task1_with_salary)
# print(task1_older)
# Task 2
# print(task2_employees)
# print(json_employees)
# print(more_employees)
# Task 3
# print(first_three)
# print(last_two)
# print(employee_shape)
# Task 4
# print(dirty_data)
# print(clean_data)
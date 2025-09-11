# Task 3

import csv

with open('../csv/employees.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

# data[0] is the header

# Create a list of full names (first_name + " " + last_name), excluding the header.
names = [row[1] + " " + row[2] for row in data[1:]]

print("List of full names:")
print(names)

# Filter names that include the letter "e."
names_with_e = [name for name in names if 'e' in name.lower()]

print("\nNames that include the letter 'e':")
print(names_with_e)

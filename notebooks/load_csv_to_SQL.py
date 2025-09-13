import csv

# Input CSV file and output SQL file
csv_file = "data/patients.csv"
sql_file = "data/insert_patients.sql"
table_name = "Patients"
batch_size = 1000 # Insert can take only a maximum of 1000 rows

with open(csv_file, mode="r", encoding="utf-8") as infile, open(sql_file, mode="w", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)

    values = []
    count = 0
    batch_num = 1

    for row in reader:
        # Escape single quotes
        name = row["Name"].replace("'", "''")
        gender = row["Gender"].replace("'", "''")
        chronic = row["ChronicCondition"].replace("'", "''")
        postcode = row["Postcode"].replace("'", "''")

        # Add row tuple
        value = f"({row['PatientID']}, '{name}', {row['Age']}, '{gender}', '{chronic}', '{postcode}')"
        values.append(value)
        count += 1

        # If batch is full, write insert statement
        if count % batch_size == 0:
            outfile.write(f"INSERT INTO {table_name} (PatientID, Name, Age, Gender, ChronicCondition, Postcode)\nVALUES\n")
            outfile.write(",\n".join(values) + ";\n\n")
            values = []  # reset batch
            batch_num += 1

    # Write any leftover rows
    if values:
        outfile.write(f"INSERT INTO {table_name} (PatientID, Name, Age, Gender, ChronicCondition, Postcode)\nVALUES\n")
        outfile.write(",\n".join(values) + ";\n\n")

print(f"SQL insert statements written to {sql_file}")



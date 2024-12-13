
from helper.CRUD_functions import (
    load_medical_database,
    create_record,
    read_records,
    update_record,
    delete_record,
)

# Sample data to test
db_file_path = "medical_records_DB.db"
new_patient_data = (
    "Johnny Doe",
    "1980-01-01",
    "M",
    "diabetes",
    "metformin",
    "penicillin",
    "2024-10-01",
)
patient_data = (
    5,
    "Anna Lee",
    "1979-05-05",
    "F",
    "asthma",
    "inhaler",
    "peanuts",
    "2022-09-19",
)


if __name__ == "__main__":
    load_medical_database()  # Load the CSV data into the database
    create_record(db_file_path, patient_data)  # Create a new record
    read_records(db_file_path)  # Read records from the database
    update_record(db_file_path, 1, new_patient_data)  # Update a record with ID 1
    delete_record(db_file_path, 5)  # Delete the record with ID 5

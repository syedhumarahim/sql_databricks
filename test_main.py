import sqlite3
from helper.CRUD_functions import (
    load_medical_database,
    create_record,
    read_records,
    update_record,
    delete_record,
)


def test_load_medical_database():
    data = load_medical_database()
    conn = sqlite3.connect(data)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medical_records")
    loaded_data = cursor.fetchall()

    if loaded_data:
        print("Database loading successful:")
        for row in loaded_data:
            print(row)
        assert len(loaded_data) > 0, "Database is empty"
    else:
        print("Failed to load the database")

    conn.close()


def test_create_record():
    # Sample data for a new record
    patient_data = (
        99,
        "Test Patient",
        "1980-01-01",
        "M",
        "test condition",
        "test medication",
        "test allergy",
        "2023-01-01",
    )
    create_record("medical_records_DB.db", patient_data)

    # Verify that the record was created
    conn = sqlite3.connect("medical_records_DB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_records WHERE patient_id = ?", (99,))
    created_record = cursor.fetchone()

    assert created_record is not None, "Failed to create the record"
    print("Record created successfully:", created_record)

    conn.close()


def test_read_records():
    database = "medical_records_DB.db"

    data = read_records(database)

    if data:
        print("Data retrieval result:")
        for row in data:
            print(row)

        assert len(data) > 0, "Data is empty"
        print("Test read_records passed successfully.")
    else:
        print("Failed to retrieve data")


def test_update_record():
    db_file = "medical_records_DB.db"

    # Sample new data to update
    new_data = (
        "Updated Patient",
        "1990-01-01",
        "F",
        "updated condition",
        "updated medication",
        "updated allergy",
        "2024-01-01",
    )
    patient_id = 1  # ID of the record to update

    update_record(db_file, patient_id, new_data)

    # Retrieve the updated data
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_records WHERE patient_id = ?", (patient_id,))
    updated_result = cursor.fetchone()

    # Print the updated and expected results
    expected_data = (patient_id,) + new_data
    print("Updated result:", updated_result)
    print("Expected result:", expected_data)

    # Assert statement to compare the updated result with the expected result
    assert updated_result == expected_data, "Data update failed"

    conn.close()


def test_delete_record():
    db_file = "medical_records_DB.db"

    # ID of the record to delete
    patient_id = 99

    delete_record(db_file, patient_id)

    # Verify that the record was deleted
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_records WHERE patient_id = ?", (patient_id,))
    deleted_result = cursor.fetchone()

    conn.close()

    assert deleted_result is None, "Data deletion failed"
    print("Record deleted successfully.")


test_load_medical_database()
test_create_record()
test_read_records()
test_update_record()
test_delete_record()

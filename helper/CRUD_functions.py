
import sqlite3
import csv
# Function to load database from CSV file
def load_medical_database(dataset="data/medical_records.csv", encoding="utf-8"):
    data = csv.reader(open(dataset, newline="", encoding=encoding), delimiter=",")
    next(data)  # Skip header
    conn = sqlite3.connect("medical_records_DB.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS medical_records")
    c.execute(
        """
        CREATE TABLE medical_records (
            patient_id INTEGER,
            name TEXT,
            date_of_birth TEXT,
            gender TEXT,
            medical_conditions TEXT,
            medications TEXT,
            allergies TEXT,
            last_appointment_date TEXT
        )
    """
    )
    # insert data
    c.executemany(
        """
        INSERT INTO medical_records (
        patient_id, name, date_of_birth, gender, medical_conditions, medications, allergies, last_appointment_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        data,
    )
    print("database loaded")

    print("Running Test Query:")
    
    print("Fetching patients with asthma")
    c.execute("SELECT * FROM medical_records WHERE medical_conditions LIKE '%asthma%';") #fetching patients with asthma
    conn.commit()
    conn.close()
    return "medical_records_DB.db"


# Create operation
def create_record(database, data):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medical_records (patient_id, name, date_of_birth, gender, medical_conditions, medications, allergies, last_appointment_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        data
        )
    
    
    conn.commit()

    cursor.execute("SELECT * FROM medical_records")
    all_records = cursor.fetchall()
    print("Database content (create):")
    for record in all_records:
        print(record)

    conn.close()

    print("Record has been successfully created.")


# Read operation
def read_records(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medical_records WHERE medical_conditions LIKE '%asthma%';") #fetching patients with asthma
    results = cursor.fetchall()

    conn.close()

    print("Database content (read):")
    for record in results:
        print(record)

    return results


# Update operation
def update_record(database, patient_id, new_data):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE medical_records SET name = ?, date_of_birth = ?, gender = ?, medical_conditions = ?, medications = ?, allergies = ?, last_appointment_date = ? WHERE patient_id = ?",
        (*new_data, patient_id)
    )

    conn.commit()

    # cursor.execute("SELECT * FROM medical_records")
    all_records = cursor.fetchall()
    print("Database content (update):")
    for record in all_records:
        print(record)

    conn.close()

    print("Record has been successfully updated.")


# Delete operation
def delete_record(database, patient_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM medical_records WHERE patient_id=?", (patient_id,))

    conn.commit()

    # cursor.execute("SELECT * FROM medical_records")
    all_records = cursor.fetchall()
    print("Database content (delete):")
    for record in all_records:
        print(record)

    conn.close()

    print("Record has been successfully deleted.")
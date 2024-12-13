import subprocess

def test_extract():
    """Test extract()"""
    result = subprocess.run(
        ["python", "main.py", "extract"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0
    assert "Extracting data..." in result.stdout


def test_load():
    """Test load()"""
    result = subprocess.run(
        ["python", "main.py", "load"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0
    assert "Transforming data..." in result.stdout


def test_query():
    """Test general query for medical records"""
    result = subprocess.run(
        [
            "python",
            "main.py",
            "query",
            """
            WITH recent_appointments AS (
                SELECT 
                    patient_id, 
                    name, 
                    COUNT(*) AS total_appointments,
                    MAX(last_appointment_date) AS last_appointment
                FROM MedicalRecords1DB
                GROUP BY patient_id, name
            ),
            combined_data AS (
                SELECT 
                    patient_id, 
                    name, 
                    total_appointments,
                    last_appointment
                FROM recent_appointments
                UNION ALL
                SELECT 
                    patient_id, 
                    name, 
                    COUNT(*) AS total_appointments,
                    MAX(last_appointment_date) AS last_appointment
                FROM MedicalRecordsOthersDB
                GROUP BY patient_id, name
            )
            SELECT 
                patient_id, 
                name, 
                total_appointments, 
                last_appointment
            FROM combined_data
            ORDER BY total_appointments DESC
            LIMIT 10;
            """,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0

test_extract()
test_load()
test_query()

import os
import requests
import pandas as pd
import os
from databricks import sql
from dotenv import load_dotenv
import subprocess


def extract(url="https://github.com/syedhumarahim/syedhumarahim-dataset_medical_records/blob/main/medical_records_1.csv",
    url_2="https://github.com/syedhumarahim/syedhumarahim-dataset_medical_records/blob/main/medical_records_others.csv",
    file_path="data/medical_records_1.csv",
    file_path_2="data/medical_records_others.csv"):
    if not os.path.exists("data"):
        os.makedirs("data")
    with requests.get(url) as r:
        with open(file_path, "wb") as f:
            f.write(r.content)
    with requests.get(url_2) as r:
        with open(file_path_2, "wb") as f:
            f.write(r.content)
    df = pd.read_csv(file_path)
    df_2 = pd.read_csv(file_path_2)

    df_subset = df.head(100)
    df_subset_2 = df_2.head(100)

    df_subset.to_csv(file_path, index=False)
    df_subset_2.to_csv(file_path_2, index=False)
    return file_path, file_path_2



# Define a global variable for the log file
LOG_FILE = "query_log.md"


def add_to_markdown(query, result="none"):
    """adds to a query markdown file"""
    with open(LOG_FILE, "a") as file:
        file.write(f"```sql\n{query}\n```\n\n")
        file.write(f"```response from databricks\n{result}\n```\n\n")


def query(query):
    load_dotenv()
    server_h = os.getenv("SERVER_HOSTNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    http_path = "/sql/1.0/warehouses/2d6f41451e6394c0"
    with sql.connect(
        server_hostname=server_h,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        c = connection.cursor()
        c.execute(query)
        result = c.fetchall()
    c.close()
    add_to_markdown(f"{query}", result)



# load the csv file and insert into databricks
def load(dataset="data/medical_records_1.csv", dataset_2="data/medical_records_others.csv"):
    payload = pd.read_csv(dataset, delimiter=",", skiprows=1)
    payload2 = pd.read_csv(dataset_2, delimiter=",", skiprows=1)
    load_dotenv(dotenv_path='.env')
    server_hostname = os.getenv("SERVER_HOSTNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    http_path = "/sql/1.0/warehouses/2d6f41451e6394c0"
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        c = connection.cursor()

        # Create and load first table
        c.execute("SHOW TABLES FROM default LIKE 'medical_records_1*'")
        result = c.fetchall()
        if not result:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS MedicalRecords1DB (
                    patient_id int,
                    name string,
                    date_of_birth string,
                    gender string,
                    medical_conditions string,
                    medications string,
                    allergies string,
                    last_appointment_date string
                )
                """
            )
            for _, row in payload.iterrows():
                convert = tuple(row)
                c.execute(f"INSERT INTO MedicalRecords1DB VALUES {convert}")

        # Create and load second table
        c.execute("SHOW TABLES FROM default LIKE 'medical_records_others*'")
        result = c.fetchall()
        if not result:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS MedicalRecordsOthersDB (
                    patient_id int,
                    name string,
                    date_of_birth string,
                    gender string,
                    medical_conditions string,
                    medications string,
                    allergies string,
                    last_appointment_date string
                )
                """
            )
            for _, row in payload2.iterrows():
                convert = tuple(row)
                c.execute(f"INSERT INTO MedicalRecordsOthersDB VALUES {convert}")
        c.close()

    return "success"

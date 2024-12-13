import csv
import os
from dotenv import load_dotenv
from databricks import sql

# load
def load_database(dataset="data/student_performance.csv", encoding="utf-8"):
    payload = csv.reader(open(dataset, newline=""), delimiter=",")
    next(payload)

    load_dotenv()
    with sql.connect(server_hostname = os.getenv("SERVER_HOSTNAME"),
                     http_path = "/sql/1.0/warehouses/2d6f41451e6394c0",
                     access_token = os.getenv("DATABRICKS_KEY")) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS student_performance")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS student_performance (
                    StudentID int,
                    Name string,
                    Gender string,
                    AttendanceRate int,
                    StudyHoursPerWeek int,
                    PreviousGrade int,
                    ExtracurricularActivities int,
                    ParentalSupport string,
                    FinalGrade int
                );
            """
            )
            string_sql = "INSERT INTO student_performance VAlUES"
            for i in payload:
                string_sql += "\n" + str(tuple(i)) + ","
            string_sql = string_sql[:-1] + ";"
            cursor.execute(string_sql)
            
            cursor.close()
            connection.close()
    return "Load Success"


if __name__ == '__main__':
    load_database()
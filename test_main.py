from mylib.extract import extract
from mylib.transform import load_database
from mylib.query import query
import os
from dotenv import load_dotenv
from databricks import sql


def test_extract():
    ext = extract()
    assert ext is not None


def test_load():
    load_dotenv()
    load = load_database()
    with sql.connect(
        server_hostname=os.getenv("SERVER_HOSTNAME"),
        http_path="/sql/1.0/warehouses/2d6f41451e6394c0",
        access_token=os.getenv("DATABRICKS_KEY"),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM student_performance")
            result = cursor.fetchall()
            cursor.close()
            connection.close()
    assert load == "Load Success"
    assert result is not None


def test_query():
    qt = query()
    complex_query = """
SELECT
    s1.ParentalSupport,
    AVG(s1.ExtracurricularActivities) AS activity,
    AVG(s1.PreviousGrade) AS previous_grade,
    AVG(s1.FinalGrade) AS final_grade
FROM default.student_performance AS s1
JOIN default.student_performance AS s2
    USING (Name)
GROUP BY s1.ParentalSupport
ORDER BY s1.ParentalSupport DESC;
"""

    load_dotenv()
    with sql.connect(
        server_hostname=os.getenv("SERVER_HOSTNAME"),
        http_path="/sql/1.0/warehouses/2d6f41451e6394c0",
        access_token=os.getenv("ACCESS_TOKEN"),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(complex_query)
            result = cursor.fetchall()
    assert result is not None
    assert qt == "Query Success"


test_extract()
test_load()
test_query()
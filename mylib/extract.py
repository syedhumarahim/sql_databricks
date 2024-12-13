import requests


def extract(
    url="https://raw.githubusercontent.com/nogibjj/Mu-Niu-Pandas-Descriptive-Statistics-Script/main/student_performance.csv",
    file_path="data/student_performance.csv",
):
    """ "Extract a url to a file path"""
    with requests.get(url) as r:
        with open(file_path, "wb") as f:
            f.write(r.content)
    return file_path
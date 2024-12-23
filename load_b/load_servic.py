import csv
from DB.postges_db.db import session

from config import load_b


def load_all_csv_b():
    # data = load_csv()
    # for row in data:
    #
    #
    # session.commit()
    # session.close()
    pass


def load_csv():
    csv_file = load_b
    with open(csv_file, mode="r", encoding="windows-1252") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data



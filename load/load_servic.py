import csv
from DB.postges_db.db import session
from DB.postges_db.models.attack_model import Attack
from DB.postges_db.models.date_model import EventDate
from DB.postges_db.models.event_model import Event
from DB.postges_db.models.gname_model import Gname
from DB.postges_db.models.location_model import Location
from DB.postges_db.models.target_model import Target
from config import load


def load_all_csv():
    data = load_csv(load)
    for row in data:
        date = insert_date(row)
        location = insert_location(row)
        attack = insert_attack(row)
        target = insert_target(row)
        gname = insert_gname(row)
        insert_event(attack, date, gname, location, row, target)

    session.commit()
    session.close()


def load_csv(csv_file):
    with open(csv_file, mode="r", encoding="windows-1252") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data


def insert_event(attack, date, gname, location, row, target):
    nkill = to_float(row.get("nkill"))
    nwound = to_float(row.get("nwound"))
    nperps = to_int(row.get("nperps"))

    # אם הערך הוא None או פחות או שווה ל-0, נהפוך אותו ל-NULL
    nkill = None if (nkill is None or nkill < 0) else nkill
    nwound = None if (nwound is None or nwound < 0) else nwound
    nperps = None if (nperps is None or nperps < 0) else nperps

    summary = row.get("summary")  # קבלת הערך של summary מתוך שורת ה-CSV

    event = Event(
        nkill=nkill,
        nwound=nwound,
        nperps=nperps,
        date=date,
        location=location,
        attack=attack,
        target=target,
        gname=gname,
        summary=summary  # הכנסה של ה-summary
    )
    session.add(event)


def insert_gname(row):
    gname_value = row["gname"]
    # אם הגנום הוא "Unknown", נשנה אותו ל-None
    if gname_value == "Unknown":
        gname_value = None

    gname = session.query(Gname).filter_by(
        gname=gname_value
    ).first()

    if not gname and gname_value is not None:
        gname = Gname(
            gname=gname_value
        )
        session.add(gname)

    return gname


def insert_target(row):
    target = session.query(Target).filter_by(
        targetype1=row["targtype1"],
        targetype1_txt=row["targtype1_txt"]
    ).first()
    if not target:
        target = Target(
            targetype1=row["targtype1"],
            targetype1_txt=row["targtype1_txt"]
        )
        session.add(target)
    return target


def insert_attack(row):
    attacktype1 = row["attacktype1"]
    attacktype1_txt = row["attacktype1_txt"]

    # אם אחד מהערכים שווה ל-"Unknown", נניח אותו כ-None
    if attacktype1 == "Unknown":
        attacktype1 = None
    if attacktype1_txt == "Unknown":
        attacktype1_txt = None

    attack = session.query(Attack).filter_by(
        attacktype1=attacktype1,
        attacktype1_txt=attacktype1_txt
    ).first()

    if not attack:
        attack = Attack(
            attacktype1=attacktype1,
            attacktype1_txt=attacktype1_txt
        )
        session.add(attack)

    return attack


def insert_location(row):
    latitude = to_float(row.get("latitude"))
    longitude = to_float(row.get("longitude"))

    location = session.query(Location).filter_by(
        region=to_int(row["region"]),
        region_txt=row["region_txt"],
        country=to_int(row["country"]),
        country_txt=row["country_txt"],
        latitude=latitude,
        longitude=longitude
    ).first()

    if not location:
        location = Location(
            region=to_int(row["region"]),
            region_txt=row["region_txt"],
            country=to_int(row["country"]),
            country_txt=row["country_txt"],
            latitude=latitude,
            longitude=longitude
        )
        session.add(location)

    return location


def insert_date(row):
    iyear = to_int(row.get("iyear"))
    imonth = to_int(row.get("imonth"))
    iday = to_int(row.get("iday"))

    # אם החודש הוא 0, נהפוך אותו ל-NULL
    imonth = None if imonth == 0 else imonth

    # אם היום הוא 0, נהפוך אותו ל-1
    iday = 1 if iday == 0 else iday

    date = session.query(EventDate).filter_by(
        iyear=iyear,
        imonth=imonth,
        iday=iday
    ).first()
    if not date:
        date = EventDate(
            iyear=iyear,
            imonth=imonth,
            iday=iday
        )
        session.add(date)
    return date


def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

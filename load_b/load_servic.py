from datetime import datetime
from DB.postges_db.db import session
from DB.postges_db.models.attack_model import Attack
from DB.postges_db.models.date_model import EventDate
from DB.postges_db.models.event_model import Event
from DB.postges_db.models.gname_model import Gname
from DB.postges_db.models.location_model import Location
from DB.postges_db.models.target_model import Target
from config import load_b
from load.load_servic import load_csv


def load_all_csv_b():
    data = load_csv(load_b)
    for row in data:
        date = insert_date(row)
        location = insert_location(row)
        attack = insert_attack(row)
        target = insert_target(row)  # Will insert with NULL values
        gname = insert_gname(row)
        insert_event(attack, date, gname, location, row, target)

    session.commit()
    session.close()





def parse_date(date_str):
    try:
        # Parse date in format "DD-Mon-YY"
        date_obj = datetime.strptime(date_str, "%d-%b-%y")
        return {
            'iyear': date_obj.year,
            'imonth': date_obj.month,
            'iday': date_obj.day
        }
    except (ValueError, TypeError):
        return {
            'iyear': None,
            'imonth': None,
            'iday': None
        }


def insert_event(attack, date, gname, location, row, target):
    nkill = to_float(row.get("Fatalities"))
    nwound = to_float(row.get("Injuries"))
    nperps = to_float(row.get("Perpetrator")) if row.get("Perpetrator") != "Unknown" else None

    # נקיון ערכים שליליים כמו בקוד המקורי
    nkill = None if (nkill is None or nkill < 0) else nkill
    nwound = None if (nwound is None or nwound < 0) else nwound
    nperps = None if (nperps is None or nperps < 0) else nperps

    event = Event(
        nkill=nkill,
        nwound=nwound,
        nperps=nperps,
        date=date,
        location=location,
        attack=attack,
        target=target,
        gname=gname
    )
    session.add(event)


def insert_gname(row):
    gname_value = row.get("Perpetrator")
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
    # מכיוון שאין מידע על target בCSV החדש, ניצור רשומה ריקה
    target = Target(
        targetype1=None,
        targetype1_txt=None
    )
    session.add(target)
    return target


def insert_attack(row):
    weapon = row.get("Weapon")
    if weapon == "Unknown":
        weapon = None

    attack = session.query(Attack).filter_by(
        attacktype1=None,  # אין לנו את המספר המקורי
        attacktype1_txt=weapon
    ).first()

    if not attack:
        attack = Attack(
            attacktype1=None,
            attacktype1_txt=weapon
        )
        session.add(attack)

    return attack


def insert_location(row):
    location = session.query(Location).filter_by(
        region=None,  # אין לנו מידע על region
        region_txt=None,
        country=None,  # אין לנו את המספר המקורי
        country_txt=row["Country"],
        latitude=None,  # אין לנו מידע על coordinates
        longitude=None
    ).first()

    if not location:
        location = Location(
            region=None,
            region_txt=None,
            country=None,
            country_txt=row["Country"],
            latitude=None,
            longitude=None
        )
        session.add(location)

    return location


def insert_date(row):
    date_parts = parse_date(row["Date"])

    date = session.query(EventDate).filter_by(
        iyear=date_parts['iyear'],
        imonth=date_parts['imonth'],
        iday=date_parts['iday']
    ).first()

    if not date:
        date = EventDate(
            iyear=date_parts['iyear'],
            imonth=date_parts['imonth'],
            iday=date_parts['iday']
        )
        session.add(date)
    return date


def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


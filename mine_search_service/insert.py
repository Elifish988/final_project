from elasticsearch import Elasticsearch
from DB.postges_db.db import session
from DB.postges_db.models.event_model import Event

es = Elasticsearch(["http://localhost:9200"])


# יצירת index אם לא קיים
def create_index():
    if not es.indices.exists(index="events"):
        es.indices.create(index="events")


def insert_data_to_elasticsearch():
    create_index()

    events = session.query(Event).all()

    for event in events:
        document = {
            "summary": event.summary,
            "region_txt": event.location.region_txt,
            "country_txt": event.location.country_txt,
            "gname": event.gname.gname if event.gname else None,
            "attacktype1_txt": event.attack.attacktype1_txt,
            "targetype1_txt": event.target.targetype1_txt
        }

        es.index(index="events", document=document)
        print(document)


# העברת הנתונים לאלסטיק
insert_data_to_elasticsearch()
from DB.postges_db.db import session
from DB.postges_db.models.attack_model import Attack
from DB.postges_db.models.event_model import Event
from DB.postges_db.models.gname_model import Gname
from DB.postges_db.models.location_model import Location
from DB.postges_db.models.target_model import Target


def shared_to_targets_service(region=None, country=None):
    query = session.query(
        Location.region_txt,
        Location.country_txt,
        Target.targetype1_txt,
        Gname.gname
    ).join(Event, Event.location_id == Location.id) \
        .join(Target, Event.target_id == Target.id) \
        .join(Gname, Event.gname_id == Gname.id)

    if region:
        query = query.filter(Location.region_txt == region)
    if country:
        query = query.filter(Location.country_txt == country)

    data = query.all()
    result = {}
    for row in data:
        target = row.targetype1_txt
        gname = row.gname
        if target not in result:
            result[target] = set()
        result[target].add(gname)

    sorted_result = sorted(result.items(), key=lambda x: len(x[1]), reverse=True)
    return [{"target": target, "groups": list(groups)} for target, groups in sorted_result]


def shared_attack_strategies_by_region_service():
    query = session.query(Location.country_txt, Attack.attacktype1_txt, Gname.gname) \
        .join(Event, Event.location_id == Location.id) \
        .join(Target, Event.target_id == Target.id) \
        .join(Gname, Event.gname_id == Gname.id) \
        .join(Attack, Event.attack_id == Attack.id)

    data = query.all()
    country_strategy_map = {}
    # setdefault = הכנסה רק אם לא קיים
    for country_txt, attack_type, group in data:
        country_strategy_map.setdefault(country_txt, {}).setdefault(attack_type, set()).add(group)

    return {
        region: [
            {"attack_type": attack_type, "groups": list(groups)}
            for attack_type, groups in attack_types.items() if len(groups) > 1
        ]
        for region, attack_types in country_strategy_map.items() if any(len(groups) > 1 for groups in attack_types.values())
    }


def groups_with_similar_target_preferences_service():
    target_groups = {}

    # שליפת כל האירועים ומיון הקבוצות לפי המטרות שהן תוקפות
    for event in session.query(Event).all():
        gname = event.gname
        target_type = event.target.targetype1_txt

        # הוספת המטרה לקבוצה אם היא לא קיימת
        if gname not in target_groups:
            target_groups[gname] = set()

        target_groups[gname].add(target_type)

    # חיפוש קבוצות עם העדפות דומות (יותר מסוג אחד של מטרות)
    similar_groups = {gname: target_types for gname, target_types in target_groups.items() if len(target_types) > 1}

    return similar_groups




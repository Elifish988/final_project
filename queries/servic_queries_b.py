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


def get_shared_attack_strategies_by_region():
    query = session.query(Location.region_txt, Attack.attacktype1_txt, Gname.gname) \
        .join(Event, Event.location_id == Location.id) \
        .join(Target, Event.target_id == Target.id) \
        .join(Gname, Event.gname_id == Gname.id) \
        .join(Attack, Event.attack_id == Attack.id)

    data = query.all()
    region_strategy_map = {}

    for region, attack_type, group in data:
        region_strategy_map.setdefault(region, {}).setdefault(attack_type, set()).add(group)

    return {
        region: [
            {"attack_type": attack_type, "groups": list(groups)}
            for attack_type, groups in attack_types.items() if len(groups) > 1
        ]
        for region, attack_types in region_strategy_map.items() if any(len(groups) > 1 for groups in attack_types.values())
    }

print(get_shared_attack_strategies_by_region())
import pandas as pd
from DB.postges_db.db import session
from DB.postges_db.models.attack_model import Attack
from DB.postges_db.models.date_model import Date
from DB.postges_db.models.event_model import Event
from DB.postges_db.models.gname_model import Gname
from DB.postges_db.models.location_model import Location
from DB.postges_db.models.target_model import Target

attack_df = pd.read_sql(session.query(Attack).statement, session.bind)
date_df = pd.read_sql(session.query(Date).statement, session.bind)
event_df = pd.read_sql(session.query(Event).statement, session.bind)
gname_df = pd.read_sql(session.query(Gname).statement, session.bind)
location_df = pd.read_sql(session.query(Location).statement, session.bind)
target_df = pd.read_sql(session.query(Target).statement, session.bind)


def get_top_deadliest_attacks_service(top):
    merged_df = event_df.merge(attack_df, left_on='attack_id', right_on='id', how='left')
    merged_df['fatality_score'] = find_fatality_score(merged_df)
    df_grouped = merged_df.groupby('attacktype1_txt')['fatality_score'].sum().reset_index()
    df_sorted = df_grouped.sort_values(by='fatality_score', ascending=False)

    if top == 'top_5':
        return df_sorted.head(5)
    else:
        return df_sorted



def get_avg_casualties_by_region_service(top):
    merged_df = event_df.merge(location_df, left_on='location_id', right_on='id', how='left')
    merged_df['casualty_score'] = find_fatality_score(merged_df)

    avg_casualties = (
        merged_df.groupby('country_txt')['casualty_score'].mean().reset_index()
        .rename(columns={'casualty_score': 'avg_casualties'})
    )

    avg_casualties_sorted = avg_casualties.sort_values(by='avg_casualties', ascending=False)

    if top == 'top_5':
        return avg_casualties_sorted.head(5)
    else:
        return avg_casualties_sorted



def get_top_5_gnames_by_casualties_service():
    merged_df = event_df.merge(gname_df, left_on='gname_id', right_on='id', how='left')
    merged_df['fatality_score'] = merged_df['nkill'] + merged_df['nwound']

    gname_grouped = merged_df.groupby('gname')['fatality_score'].sum().reset_index()
    gname_sorted = gname_grouped.sort_values(by='fatality_score', ascending=False)

    return gname_sorted.head(5)



def get_percentage_change_in_attacks_by_country_service(top='all'):
    merged_df = event_df.merge(date_df, left_on='date_id', right_on='id', how='left')
    merged_df = merged_df.merge(location_df, left_on='location_id', right_on='id', how='left')

    yearly_country_attacks = merged_df.groupby(['country_txt', 'iyear'])['id'].count().reset_index().rename(columns={'id': 'attack_count'})
    yearly_country_attacks['percentage_change'] = yearly_country_attacks.groupby('country_txt')['attack_count'].pct_change() * 100
    yearly_country_attacks_sorted = yearly_country_attacks.sort_values(by='percentage_change', ascending=False)

    # שלב 5: סינון על פי הבחירה (Top-5 או הכל)
    if top == 'top_5':
        return yearly_country_attacks_sorted.groupby('country_txt').head(5)
    else:
        return yearly_country_attacks_sorted




def get_most_active_groups_by_region_service(country_txt=None):
    merged_df = event_df.merge(location_df, left_on='location_id', right_on='id', how='left')
    merged_df = merged_df.merge(gname_df, left_on='gname_id', right_on='id', how='left')
    if country_txt:
        merged_df = merged_df[merged_df['country_txt'] == country_txt]
    group_activity = merged_df.groupby('gname')['id'].count().reset_index().rename(columns={'id': 'event_count'})
    sorted_group_activity = group_activity.sort_values(by='event_count', ascending=False)

    return sorted_group_activity






def find_fatality_score(merged_df):
    return merged_df['nkill'] * 2 + merged_df['nwound']
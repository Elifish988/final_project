from mine_search_service.insert import insert_data_to_elasticsearch, es


def search_events_by_text(query_text):
    response = es.search(
        index="events",
        body={
            "query": {
                "multi_match": {
                    "query": query_text,
                    "fields": ["summary", "region_txt", "country_txt", "gname", "attacktype1_txt", "targetype1_txt"]
                }
            }
        }
    )

    return response['hits']['hits']



result = search_events_by_text("terror attack")
for event in result:
    print(event['_source'])

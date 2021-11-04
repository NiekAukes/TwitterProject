import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "AAAAAAAAAAAAAAAAAAAAACaIVQEAAAAA3Tg9sYHP9NP92ybRW3FLeUcHUHI%3D39GTmCAilHv366T72l2yZky9EHhW0NIbB37geJajnm7OcG50cM"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "#weer", "tag": "weer tweather"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set, callback):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            callback(json_response)

tweet_fields = "tweet.fields=author_id,geo,id,created_at,entities,source"
expansions = "expansions=author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id"
user_fields = "user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
place_fields = "place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type"


rules = get_rules()
delete = delete_all_rules(rules)
set = set_rules(delete)

def SearchTweets(query, maxresults):
    url = "https://api.twitter.com/2/tweets/search/recent?query=" + str(query)
    
    more = "&max_results=" + str(maxresults)
    payload={}
    headers = {}

    response = requests.request("GET","{}&{}&{}&{}&{}".format(url, tweet_fields, expansions, user_fields, more), data=payload, auth=bearer_oauth)
    json_obj = json.loads(response.text)
    if json_obj['meta']['result_count'] < 1:
        return []
    return json_obj
if __name__ == "__main__":
    a = SearchTweets("weer", 10)
    print(a)
    pass
    #get_stream(set, cback)
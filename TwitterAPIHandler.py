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
        {"value": "weer", "tag": "weer tweather"},
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
def cback(json_file):
    id = "1455648455347642368"
    url = "https://api.twitter.com/2/tweets/{}?{}&{}&{}&{}".format(id, expansions, tweet_fields, user_fields, place_fields)


    resp = requests.request("GET", url, auth=bearer_oauth)

    if resp.status_code != 200:
        print(
            "Request returned an error: {} {}".format(
                resp.status_code, resp.text
            )
        )
        return
    try:
        tweetdata = json.loads(resp.content)
        tweetincl = tweetdata['includes']
        tweetdata = tweetdata['data']
        print(tweetdata['text'])
        #parse data into accepted format
        #data needed:
        #   tweet.user.screen_name
        #   tweet.user.name
        #   tweet.user.profile_image_url
        #   tweet.created_at
        #   tweet.text
        #   tweet.entities
    
    except:
        return
    from datetime import datetime
    twet = {}
    twet['user'] = {}
    twet['user']['screen_name'] = tweetincl['users'][0]['username']
    twet['user']['name'] = tweetincl['users'][0]['name']
    twet['user']['profile_image_url'] = tweetincl['users'][0]['profile_image_url']
    twet['created_at'] = datetime.strptime(tweetdata['created_at'], "%Y-%m-%dT%H:%M:%S.000Z").strftime('%a %b %d %H:%M:%S %z %Y')
    twet['text'] = tweetdata['text']
    twet['entities'] = {}
    twet['entities']['hashtags'] = []
    twet['entities']['user_mentions'] = []
    twet['entities']['urls'] = []
    for item in tweetdata['entities']['hashtags']:
        twet['entities']['hashtags'].append({"text":item['tag'], "indices":[item['start'], item['end']]})
    for item in tweetdata['entities']['mentions']:
        twet['entities']['user_mentions'].append({"id_str":item["id"],"id":int(item["id"]),"screen_name":item['username'],"name":item['username'], "indices":[item['start'], item['end']]})
    for item in tweetdata['entities']['urls']:
        twet['entities']['urls'].append({"url":item['url'],"display_url":item['display_url'], "indices":[item['start'], item['end']]})
cback(1)

rules = get_rules()
delete = delete_all_rules(rules)
set = set_rules(delete)


if __name__ == "__main__":
    pass
    #get_stream(set, cback)
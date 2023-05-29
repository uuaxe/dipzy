import requests
import json


class Twitter:
    '''Twitter v2 API'''
    base_url = "https://api.twitter.com/2"

    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.headers = {
            "Authorization": f"Bearer {bearer_token}"
        }

    def _request(self, method, url, params={}, **kwargs):
        response = requests.request(
            method, url, headers=self.headers, params=params, **kwargs
        )
        if response.status_code != 200 and response.status_code != 201:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        return response

    # Users endpoints #

    def get_users(self, user_ids=None, usernames=None, user_fields="public_metrics"):
        '''
        Args:
            user_ids:  User IDs
            usernames: Specify the usernames that you want to lookup below.
                You can enter up to 100 comma-separated values.
            user_fields: User fields are adjustable, options include:
                created_at, description, entities, id, location, name,
                pinned_tweet_id, profile_image_url, protected,
                public_metrics, url, username, verified, and withheld
        '''
        params = {"user.fields": user_fields}
        if usernames is None:
            print("Assuming that user IDs are provided.")
            params["ids"] = user_ids,
            url = self.base_url + "/users"
        else:
            params["usernames"] = usernames
            url = self.base_url + "/users/by"

        response = self._request("GET", url, params)
        return response.json()["data"]

    def get_user_tweets(self, user_id, tweet_fields="created_at", **kwargs):
        '''
        Args:
            tweet_fields: Tweet fields are adjustable. Options include:
                attachments, author_id, context_annotations,
                conversation_id, created_at, entities, geo, id,
                in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
                possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
                source, text, and withheld
        '''
        url = self.base_url + f"/users/{user_id}/tweets"
        params = {"tweet.fields": tweet_fields}
        params.update(kwargs)
        response = self._request("GET", url, params)
        return response.json() 

    # List endpoints #

    def get_list_members(self, list_id, user_fields="created_at"):
        '''
        Args:
            user_fields: User fields are adjustable, options include:
                created_at, description, entities, id, location, name,
                pinned_tweet_id, profile_image_url, protected,
                public_metrics, url, username, verified, and withheld
        '''
        url = self.base_url + f"/lists/{list_id}/members"
        params = {"user.fields": user_fields}
        response = self._request("GET", url, params)
        return response.json() 
    
    # Rules endpoint

    def get_rules(self) -> dict:
        url = self.base_url + f"/tweets/search/stream/rules"
        response = self._request("GET", url)
        return response.json()["data"]

    def delete_all_rules(self, rules: dict) -> None:
        if rules is None or "data" not in rules:
            return None

        rule_ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": rule_ids}}
        url = self.base_url + f"/tweets/search/stream/rules"
        response = self._request("POST", url, json=payload)
        print(json.dumps(response.json()))

    def set_rules(self, rules: list) -> None:
        # You can adjust the rules if needed
        payload = {"add": rules}
        url = self.base_url + f"/tweets/search/stream/rules"
        response = self._request("POST", url, json=payload)
        print(json.dumps(response.json()))

    def get_stream(self, params={
        "tweet.fields": "created_at",
        "expansions": "author_id"
    }):
        url = self.base_url + f"/tweets/search/stream"
        response = self._request("GET", url, params, stream=True)
        return response

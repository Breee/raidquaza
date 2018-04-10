import requests

class BitlyLinkShortener(object):

    def __init__(self, access_token):
        self.api_user = ""
        self.api_key = ""
        self.access_token = access_token

    def shorten_link(self, uri):
        query_params = {
            'access_token': self.access_token,
            'longUrl': uri
        }

        endpoint = 'https://api-ssl.bitly.com/v3/shorten'
        response = requests.get(endpoint, params=query_params, verify=True)

        data = response.json()

        if not data['status_code'] == 200:
            print("Unexpected status_code: {} in bitly response. {}".format(data['status_code'], response.text))

        return data['data']['url']
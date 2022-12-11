import requests
import re
import json


class Rpilocator:
    def __init__(self, country) -> None:
        self.country = country

    def getTokens(self):
        url = 'https://rpilocator.com/?country={}'
        res = requests.get(url=url.format(self.country))
        res.raise_for_status() 

        token_text = re.findall(r"localToken=\"(.*)\"", res.text)
        cookies = res.cookies


        if len(token_text) != 1:
            raise RuntimeError("unable to retrieve token")

        return (token_text[0],cookies.get('CFID'))

    def send(self):
        token, cfid = self.getTokens()
        url = f'https://rpilocator.com/data.cfm?method=getProductTable&token={token}&country={self.country.upper()}'

        headers = {
            'cookie' : f'CFID={cfid}; CFTOKEN=0;',
            'x-requested-with': 'XMLHttpRequest'
        }

        res = requests.get(url, headers=headers)
        res.raise_for_status()

        return res.json()


class RpilocatorMock:
    def __init__(self, country) -> None:
        self.country = country

    def send(self):
        with open('mock.json') as fr:
            return json.load(fr)
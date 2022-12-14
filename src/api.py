import json
import logging
import re
import requests


class RpilocatorAPI:
    def __init__(self, country: str) -> None:
        self.country = country

    def get_tokens(self):
        url = 'https://rpilocator.com/?country={}'
        res = requests.get(url=url.format(self.country))
        res.raise_for_status() 

        token_text = re.findall(r"localToken=\"(.*)\"", res.text)
        cookies = res.cookies

        if len(token_text) != 1:
            raise RuntimeError("unable to retrieve token")

        return (token_text[0], cookies.get('CFID'))

    def send(self):
        token, cfid = self.get_tokens()
        country = self.country.upper()
        url = f'https://rpilocator.com/data.cfm?method=getProductTable&token={token}&country={country}'

        headers = {
            'cookie' : f'CFID={cfid}; CFTOKEN=0;',
            'referer': f'https://rpilocator.com/?country={country}',
            'x-requested-with': 'XMLHttpRequest'
        }

        res = requests.get(url, headers=headers)
        res.raise_for_status()
        try:
            output = res.json()
            logging.info(output)
            return output
        except Exception as e:
            logging.exception(e.message)
            return {}

class RpilocatorMock:
    def __init__(self, country: str) -> None:
        self.country = country

    def send(self):
        with open('mock.json') as fr:
            return json.load(fr)

class Rpilocator:
    @classmethod
    def send(cls, country: str, is_mock: bool):
        if is_mock:
            rpilocator_api = RpilocatorMock(country)
        else:
            rpilocator_api = RpilocatorAPI(country)
        
        return rpilocator_api.send()
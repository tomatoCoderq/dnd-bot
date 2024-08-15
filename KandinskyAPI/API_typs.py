from .URLS import ApiUrls
from .GenTyps import Image2TextGen


class ApiApi:

    urls = ApiUrls
    text2image_param = Image2TextGen()

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key

    async def get_headers(self):
        return {
            'X-Key': f'Key {self.api_key}',
            'X-Secret': f'Secret {self.secret_key}'
        }

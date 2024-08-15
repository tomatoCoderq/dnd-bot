from __future__ import annotations

import asyncio
import pybase64
import json
import time

import aiohttp

from .API_typs import ApiApi


class FusionBrainApi:
    def __init__(self, api: ApiApi):
        self.api = api

    async def get_models(self):
        async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
            url = self.api.urls.text2image_models_url
            async with session.get(url) as response:
                return await response.json()

    async def get_styles(self):
        async with aiohttp.ClientSession() as session:
            url = self.api.urls.text2image_styles
            async with session.get(url) as response:
                return await response.json()

    async def text2image(self,
                         model: str | None = None,
                         style: str | None = None,
                         width: int | None = None,
                         height: int | None = None,
                         negative_prompt: str | None = None,
                         query: str | None = None,
                         max_time: int = 120
                         ):
        model, params = await self.api.text2image_param.comb(model, style, width, height, negative_prompt, query)

        data = aiohttp.FormData()
        data.add_field("params",
                       json.dumps(params),
                       content_type="application/json",
                       )
        data.add_field("model_id", "4")
        async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
            url = self.api.urls.text2image_run_url
            async with session.post(url, data=data) as response:
                result = await response.json()

        if "error" in result:
            raise ValueError(result)

        uuid = result['uuid']

        return await self.check_generation(uuid, max_time)

    async def check_generation(self,
                               uuid: str,
                               max_time
                               ):
        start_time = time.time()
        while time.time() - (start_time + max_time) < 0:
            async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
                url = self.api.urls.text2image_status_url.replace("$uuid", uuid)
                async with session.get(url) as response:
                    result = await response.json()
                    if result['status'] == 'DONE':
                        censor = result['censored']
                        if censor:
                            raise ValueError("Запрос не соответствует фильтрам цензуры")
                        else:
                            return pybase64.b64decode(result['images'][0])

            await asyncio.sleep(5)

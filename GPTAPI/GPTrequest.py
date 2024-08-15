from typing import Union

from openai import AsyncOpenAI

from .Params import *


class RequestAPI:
    def __init__(self, client: AsyncOpenAI, model: str = 'gpt-4o-mini'):
        self.client = client
        self.model = model

    async def get_request(self,
                          request: (Union[
                              AnalyzeBF, RecommendationsBF, RecommendationsQQ, RecommendationsAC, RecommendationsLOC]),
                          data: str
                          ):
        if hasattr(request, 'type'):
            if request.type not in [
                AnalyzeBF.type, RecommendationsBF.type,
                RecommendationsQQ.type, RecommendationsAC.type,
                RecommendationsLOC.type
            ]:
                raise TypeError('Несуществующий тип запроса')
            else:
                response = await self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=
                    [
                        await request.comb(),
                        {"role": "user", "content": data}
                    ],
                    response_format=request.structure
                )
                return response.choices[0].message.parsed

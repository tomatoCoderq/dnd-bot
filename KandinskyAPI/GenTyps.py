class Image2TextGen:
    model = '3.0'
    style = 'DEFAULT'
    width = 1024
    height = 1024
    negative_prompt = ''
    query = 'Оборотень'

    async def comb(self,
                   model: str,
                   style: str,
                   width: int,
                   height: int,
                   negative_prompt: str,
                   query: str,
                   ):
        _model = self.model if model is None else model
        _style = self.style if style is None else style
        _width = self.width if width is None else width
        _height = self.height if height is None else height
        _negative_prompt = self.negative_prompt if negative_prompt is None else negative_prompt
        _query = self.query if query is None else query

        return [
            _model,
            {
                "type": "GENERATE",
                "style": _style,
                "width": _width,
                "height": _height,
                "negativePromptUnclip": _negative_prompt,
                "generateParams": {
                    "query": _query
                }
            }
        ]

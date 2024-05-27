# -*- coding: utf-8 -*-

import logging
import aiohttp
import async_timeout
from core.exceptions.connector import CallAPIFail

from typing import Any, Dict, List


logger = logging.getLogger("uvicorn")


class BaseApiConnector:
    def __init__(self, logger):
        self.logger = logger

    async def _fetch(
        self,
        method: str,
        url: str,
        headers: Dict = {},
        params: Dict = {},
        payload: Any = None,
        files: Any = None,
        auth: Any = None,
        client_verify: bool = False,
        request_timeout: int = 180,
        return_json: bool = True,
        **kwargs
    ):
        if not method or not url:
            raise ValueError(f'missing {method=} or {url}')

        with async_timeout.timeout(request_timeout):
            async with aiohttp.ClientSession() as session:
                request = getattr(session, method.lower())
                async with request(url, json=payload, headers=headers, params=params) as response:
                    if return_json:
                        if response.status in (200, 201,):
                            res = await response.json()
                        else:
                            raise CallAPIFail(f'{self.__class__.__class__} fetch failed -> {res=}')

                    else:
                        res = response

        return res

from app.types.operator_types import RestOperator
from app.services import BaseService
from app.types.api_response import ApiResponse

import aiohttp


class Rest(BaseService):

    def __init__(self, config: RestOperator) -> None:
        self.config = config

    async def request(self, data: dict = {}) -> ApiResponse:
        kwargs = {}
        if self.config.method in ["post", "patch", "update"]:
            kwargs["json"] = self.config.data
            kwargs["json"].update(data)
        else:
            kwargs["params"] = self.config.data
            kwargs["params"].update(data)
        print(kwargs["json"])
        async with aiohttp.ClientSession() as session:
            async with session.request(
                self.config.method,
                self.config.url,
                headers=self.config.headers,
                **kwargs
            ) as response:
                print("Rest Status: " + str(response.status))
                if response.status == 200:
                    data = await response.json()
                    if data["status"]:
                        return ApiResponse(**data)
                    else:
                        message = data["message"] if data["message"] else ""
                        print("response error -> " + message )
        raise Exception("Rest service error with status code " + str(response.status))

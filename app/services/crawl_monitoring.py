from app.types.crawl_monitoring_types import CrawlMonitoringType
from app.services import BaseService
from app.types.api_response import ApiResponse

import aiohttp


class CrawlMonitoring(BaseService):
    URL = "https://api.d.aiengines.ir/crawl_monitoring/v1"

    async def request(self, method, action_url, data=None):
        kwargs = {}
        print(data)
        headers = {}
        if method in ["post", "patch", "update"]:
            kwargs["json"] = data
        else:
            kwargs["params"] = data
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, self.URL + action_url, headers=headers, **kwargs
            ) as response:
                print("Crawl Monitoring Status: " + str(response.status))
                if response.status == 200:
                    data = await response.json()
                    if data["status"]:
                        return data
                    else:
                        message = data["message"] if data["message"] else ""
                        print("response error -> " + message)
        raise Exception("Rest service error with status code " + str(response.status))

    async def creat_service_log(self, data: CrawlMonitoringType):
        project = await self.request("get", "/user/project", {"monitor_id": data.project_id})
        data.project_id = project["data"][0]["id"]
        res = await self.request("post", "/user/service", data.model_dump())
        return res

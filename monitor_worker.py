from app.models import Monitor, MontitorResult, DataSource
from app.data_source.mysql import Mysql
from app.data_source.rest import Rest
from app.data_source import BaseDataSource
from app.data_source.elasticsearch import Elasticsearch
from app import send_data_source_param
from config import TORTOISE_ORM

import asyncio
import datetime
from datetime import timezone

from tortoise import Tortoise
from tortoise import Tortoise, run_async


DATA_SOURCE = {
    "mysql": Mysql,
    "rest": Rest,
    "elasticsearch": Elasticsearch,
}


async def run_jobs(data_source, monitor: Monitor) -> None:
    try:
        data = data_source.execute(monitor.query)
        await MontitorResult.create(monitor_id=monitor.id, data=data)
    except Exception as e:
        print("Run jobs error: " + e.__str__())


async def main() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    # await Tortoise.generate_schemas()
    while True:
        print("Runing ...")
        try:
            monitors = await Monitor.filter(is_active=True)
            for monitor in monitors:
                result = (
                    await MontitorResult.filter(monitor=monitor)
                    .order_by("-id")
                    .limit(1)
                )
                if result:
                    result = result[0]
                    created_at = result.created_at.replace(tzinfo=timezone.utc)
                    date = created_at + datetime.timedelta(seconds=monitor.interval)

                if not result or date <= datetime.datetime.now(tz=timezone.utc):
                    print(
                        "**********"
                        + " Start Monitor with name: "
                        + monitor.name
                        + " **********"
                    )
                    source: DataSource = await monitor.source
                    param = send_data_source_param(source)
                    data_source: BaseDataSource = DATA_SOURCE[source.type.value](param)
                    data_source.connect()
                    await run_jobs(data_source, monitor)
                    data_source.disconnect()

            await asyncio.sleep(1)

        except TimeoutError:
            print("Time Out Error !!!")
        except Exception as e:
            print("Main func error: " + e.__str__())


if __name__ == "__main__":
    run_async(main())

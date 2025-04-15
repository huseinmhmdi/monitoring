from config import TORTOISE_ORM
from app.models import Alert, Monitor, MontitorResult, AlertResult, Operator, Project
from app.types.operator_types import (
    SmsOperator,
    CallOperator,
    EmailOperator,
    RestOperator,
)
from app.services.sms import SMS
from app.services.email import Email
from app.services.call import Call
from app.services.rest import Rest
from app.services import BaseService
from app.types.api_response import ApiResponse
from app.types.crawl_monitoring_types import CrawlMonitoringType
from app.services.crawl_monitoring import CrawlMonitoring

from tortoise import Tortoise, run_async
from jinja2 import Template

import asyncio
import datetime
from datetime import timezone


SENDER = {"sms": SMS, "email": Email, "call": Call, "rest": Rest}


async def get_path_dict(condition: str) -> str:
    path_dict = None
    value = condition.split(" ")
    for val in value:
        if val.startswith("$"):
            path_dict = val[1:]
            break
    if path_dict is None:
        raise Exception("path dict Not valid !!!")

    return path_dict


async def get_count_curl(alert: Alert, convert_time) -> str:
    monitor_result_data = await MontitorResult.filter(
        monitor_id=alert.monitor_id, created_at__gt=convert_time
    ).values_list("data", flat=True)
    count = 0
    path_dict = await get_path_dict(alert.condition)

    for data in monitor_result_data:
        tpl = Template("{{" + path_dict + "}}")
        count += int(tpl.render(data=data))

    print(f"Monitor Result Count: {count}")
    return str(count)


async def condition_convert_to_dict(condition: str, monitor_result_count: str):
    path_dict = await get_path_dict(condition)
    keys = path_dict.split(".")
    nested_dict = {}
    current_level = nested_dict

    for key in keys[:-1]:
        current_level[key] = {}
        current_level = current_level[key]

    current_level[keys[-1]] = int(monitor_result_count)
    return nested_dict["data"]


async def set_alert_result(is_passed: bool, alert: Alert):
    await AlertResult.create(is_passed=is_passed, alert=alert)


async def set_service_result(is_passed: bool, alert: Alert) -> None:
    monitor: Monitor = await alert.monitor
    project: Project = await monitor.project
    crawl_monitor = CrawlMonitoringType(
        text="",
        type="شرط",
        project_id=project.id,
        step=alert.level,
        status=is_passed,
        action="بله و خیر",
    )
    monitor = await CrawlMonitoring().creat_service_log(crawl_monitor)


async def alert_serialize(alert: Alert) -> dict:
    alert_dic = await alert.get(id=alert.id).values()
    monitor: Monitor = await alert.monitor
    project: Project = await monitor.project
    context = {}
    context.update({"project_name": project.name})
    for key in alert_dic.keys():
        _val = alert_dic[key]
        if isinstance(_val, datetime.datetime):
            _val = str(_val)

        if isinstance(_val, Alert.Status):
            _val = _val.value
        context.update({key: _val})
    return context


def send_operator_param(operator: Operator):
    match operator.type.value:
        case "sms":
            param = SmsOperator(**operator.args)
        case "call":
            param = CallOperator(**operator.args)
        case "email":
            param = EmailOperator(**operator.args)
        case "rest":
            param = RestOperator(**operator.args)
        case _:
            Exception("not valid operator type !!!")
    return param


async def update_next_alert(alert: Alert, destination: int) -> None:
    monitor: Monitor = await alert.monitor
    next_alert = await Alert.get(monitor=monitor, level=alert.level + 1)
    await next_alert.update_from_dict(
        {"duration": destination, "status": alert.Status.RESULVED.value}
    )
    await next_alert.save()


async def update_tolerance(alert: Alert, count: int):
    await alert.update_from_dict({"tolerance": count})
    await alert.save()


async def safe_condition_response(alert: Alert) -> None:
    monitor: Monitor = await alert.monitor
    await Alert.filter(monitor=monitor).exclude(level=1).update(
        status=Alert.Status.FIRING.value, tolerance=0
    )
    await Alert.filter(monitor=monitor, level=1).update(tolerance=0)


async def run_jobs(alert: Alert) -> None:
    try:
        now = datetime.datetime.now(tz=timezone.utc)
        operator: Operator = await alert.operator
        convert_time = now - datetime.timedelta(seconds=alert.duration)
        monitor_result_count = await get_count_curl(alert, convert_time)
        condition_dict = await condition_convert_to_dict(
            alert.condition, monitor_result_count
        )
        data = condition_dict
        print("data: " + str(data))
        condition = alert.condition.replace("$", "")
        tpl = Template("{{" + condition + "}}")
        is_condition = eval(tpl.render(data=data))
        print(condition)
        print("is_condition: " + str(is_condition))
        if is_condition:
            await set_alert_result(True, alert)
            await set_service_result(True, alert)
            await update_tolerance(alert, 1)
            if alert.level != 1:
                status = alert.Status.FIRING.value
            else:
                status = alert.Status.FIRING.value
            if alert.status.value != status:
                await alert.update_from_dict({"status": status})
                await alert.save()
        else:
            await set_alert_result(False, alert)
            await update_tolerance(alert, alert.tolerance + 1)
            if alert.status.value != alert.Status.FIRING.value and alert.tolerance > 2:
                if alert.status.value != alert.Status.FIRING.value:
                    await alert.update_from_dict({"status": alert.Status.FIRING.value})
                    await alert.save()
                    await update_tolerance(alert, 1)
            else:
                return None
            await set_service_result(False, alert)
        param = send_operator_param(operator)
        sender: BaseService = SENDER[operator.type.value](param)
        alert_ser = await alert_serialize(alert)
        alert_ser.update({"is_condition": is_condition})
        res: ApiResponse = await sender.request(alert_ser)
        if res.data:
            if "destnation" in res.data.keys():
                await update_next_alert(alert, res.data["destnation"])
            if "is_safe" in res.data.keys() and res.data["is_safe"]:
                await safe_condition_response()
        print("___ End ___")
    except Exception as e:
        print("Run Jobs Error: " + e.__str__())


async def main() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    while True:
        print("Runing ...")
        try:
            alerts = await Alert.filter(
                monitor__is_active=True, status=Alert.Status.RESULVED.value
            )
            for alert in alerts:
                result = await AlertResult.filter(alert=alert).order_by("-id").limit(1)

                if result:
                    result = result[0]
                    created_at = result.created_at.replace(tzinfo=timezone.utc)
                    date = created_at + datetime.timedelta(seconds=alert.duration)

                if not result or date <= datetime.datetime.now(tz=timezone.utc):
                    await run_jobs(alert)

        except TimeoutError:
            print("Time Out Error !!!")
        except Exception as e:
            print("Main func error: " + e.__str__())
        print("\n********** Reload **********\n")
        await asyncio.sleep(3)


if __name__ == "__main__":
    run_async(main())

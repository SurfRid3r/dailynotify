import requests
from bridge.reply import Reply, ReplyType
from plugins import *
from bridge.context import ContextType
import os
from common.log import logger
from plugins.dailynotify.dailynotify import register
from datetime import datetime

# 1. 每天晚上11点查询第二天天气，判断是否会下雨 =>查询3天内天气
# 2. 每3小时查询4小时内天气，判断是否会小于  => 查询24h内天气


@register("weather_notify")
def weather_notify(conf: dict, e_context: EventContext):
    qweather_api = conf.get("qweather_token")
    if not qweather_api:
        return e_context
    content = e_context["context"].content
    params = content.split(" ")
    city = params[1] if len(params) > 1 else "北京"
    weather_type = params[2] if len(params) > 2 else "hourly"
    alway_send = params[3] if len(params) > 3 else "alway_send"
    reply = Reply()
    reply.type = ReplyType.TEXT
    location_id, addr = get_city_location_qweather(city, qweather_api)
    if not location_id:
        return
    elif weather_type == "hourly":
        data, summary = get_weather_24hour_qweather(location_id, qweather_api)
        is_send, msg = check(data, "hourly")
    else:
        data, summary = get_weather_3day_qweather(location_id, qweather_api)
        is_send, msg = check(data, "daily")
    reply.content = addr + msg + "\n" + summary
    # 状态是永远发送消息或者是温，低温，雨天
    if alway_send == "alway_send" or is_send:
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS


def get_city_location_qweather(address, qweather_api):
    url = f"https://geoapi.qweather.com/v2/city/lookup?location={address}&key={qweather_api}&number=1"
    response = requests.get(url)
    data = response.json()
    if data.get("code", "404") == "200" and len(data.get("location", [])):
        logger.debug("Get city location_id success")
        loc = data["location"][0]
        addr = loc.get("adm2", "") + loc.get("adm1", "") + loc.get("name")
        location_id = loc.get("id")
        return location_id, addr
    logger.error(f"Get city location_id fail, address: {address} .")
    return None, None


def get_weather_3day_qweather(location_id, qweather_api):
    url = f"https://devapi.qweather.com/v7/weather/3d?location={location_id}&key={qweather_api}&lang=zh"
    response = requests.get(url)
    data = response.json()
    if data.get("code", "404") == "200":
        logger.debug("Get daily weather success.")
        # 生成总结
        summary = "未来三天天气预报🌡:\n"
        for day in data["daily"]:
            date = day.get("fxDate", "日期未知")
            weather = day.get("textDay", "天气未知")
            temp_max = day.get("tempMax", "高温未知")
            temp_min = day.get("tempMin", "低温未知")
            summary += f"{date}白天{weather},最高气温{temp_max}°C,最低气温{temp_min}°C\n"

        summary += f'\n详细可查看{data.get("fxLink", "https://www.qweather.com/weather/")}\n'
        return data, summary
    logger.error(f"Get daily weaether search fail, location_id: {location_id} .")
    return None, None


def get_weather_24hour_qweather(location_id, qweather_api):
    url = f"https://devapi.qweather.com/v7/weather/24h?location={location_id}&key={qweather_api}&lang=zh"
    response = requests.get(url)
    data = response.json()
    if data.get("code", "404") == "200":
        logger.debug("Get hourly weather success.")
        summary = "未来24小时天气预报🌡:\n"
        for hour in data["hourly"]:
            try:
                dt = datetime.fromisoformat(hour["fxTime"])
                dt = dt.astimezone()
                fx_hour = dt.strftime("%H时")
                # 只显示当天天气，避免消息太长
                if fx_hour == "00时":
                    break
            except (KeyError, ValueError):
                fx_hour = "时间未知"
            weather = hour.get("text", "天气未知")
            temp = hour.get("temp", "温度未知")
            summary += f"{fx_hour} {weather},气温{temp}°C\n"

        summary += f'\n详细可查看{data.get("fxLink", "https://www.qweather.com/weather/")}\n'
        return data, summary
    logger.error(f"Get hourly weaether search fail, location_id: {location_id} .")
    return None, None


def check(weather_data, type="daily"):
    """
    判断是否会下雨和判断温差
    :return:
        True,返回要发送的消息
        False,不处理
    """
    msg = ""
    if type == "daily":
        today = weather_data["daily"][0]
        tommorrow = weather_data["daily"][1]
        if int(tommorrow["tempMax"]) - int(today["tempMax"]) > 5:
            msg += f"明天最高温度:{tommorrow['tempMax']}, 比今天高多了.\n"
        if int(today["tempMin"]) - int(tommorrow["tempMin"]) > 5:
            msg += f"明天最低温度:{tommorrow['tempMin']}, 比今天低多了.\n"
        # 下雨提醒
        if "雨" in tommorrow["textDay"]:
            msg = f"明天会下{tommorrow['textDay']}🌧️,记得带伞☔。"
        # 明天与今天温差过大提醒

        return True, msg
    elif type == "hourly":
        # 4小时内
        for i in range(0, 4):
            if "雨" in weather_data["hourly"][i]["text"]:
                msg += f"{i+1}小时后会有{weather_data['hourly'][i]['text']}🌧️。"
                return True, msg
    return False, msg

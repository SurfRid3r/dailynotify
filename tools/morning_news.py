# encoding:utf-8

import requests
from bridge.reply import Reply, ReplyType
from plugins import *
from bridge.context import ContextType
from common.log import logger
from plugins.dailynotify.dailynotify import register


@register("morning_news")
def morning_news(conf: dict, e_context: EventContext):
    alapi_token = conf.get("alapi_token")
    reply = Reply()
    if not (e_context["context"].type != ContextType.TEXT or alapi_token):
        logger.error("[morning_news]需要配置alapi_token，详见http://www.alapi.cn/api/view/93")
        return e_context

    url = "https://v2.alapi.cn/api/zaobao"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = f"token={alapi_token}&format=json"
    response = requests.request("POST", url, data=payload, headers=headers).json()
    if response.get("code", 404) == 200:
        news = response.get("data", None)
        if not news:
            return e_context
        elif conf.get("type", "image") == "imag_url":
            reply.type = ReplyType.IMAGE_URL
            reply.content = news.get("image")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        # 返回文字早报
        elif conf.get("type", "image") == "text":
            reply.type = ReplyType.TEXT
            # 简单的转化为字符串
            e_context["reply"] = reply
            reply.content = "每日早报🆕:\n" + "\n".join(news.get("news"))
            e_context.action = EventAction.BREAK_PASS
    else:
        logger.error(f"[morning_news]Get morning_news fail, error code:{response.get('code')}, error msg:{response.get('msg', 'fail')}")
    return e_context

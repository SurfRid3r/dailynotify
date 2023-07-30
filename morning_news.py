# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
import requests


@plugins.register(
    name="morning_news",
    desire_priority=1,
    hidden=True,
    desc="每日早报",
    version="0.1",
    author="SurfRid3r",
)
class Morning_news(Plugin):
    def __init__(self):
        super().__init__()
        curdir = os.path.dirname(__file__)
        config_path = os.path.join(curdir, "config.json")
        if not os.path.exists(config_path):
            logger.info("[morning_news]配置文件不存在，将使用config-template.json模板")
            config_path = os.path.join(curdir, "config-template.json")

        with open(config_path, mode="r", encoding="utf-8") as f:
            self.conf = json.load(f)

        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[morning_news] inited")

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        elif not e_context["context"].content.startswith(self.conf.get("command_prefix", "/早报")):
            return
        news = self.fetch_news()
        # 返回早报图片
        reply = Reply()
        if not news:
            return 
        elif self.conf.get("type", "image") == "imag_url":
            reply.type = ReplyType.IMAGE_URL
            reply.content = news.get("head_image")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        # 返回文字早报
        elif self.conf.get("type", "image") == "text":
            reply.type = ReplyType.TEXT
            # 简单的转化为字符串
            e_context["reply"] = reply
            reply.content = "每日早报🆕:\n" + "\n".join(news.get("news"))
            e_context.action = EventAction.BREAK_PASS
        return

    def fetch_news(self):
        alapi_token = self.conf.get("alapi_token", "")
        if not alapi_token:
            logger.error("[morning_news]需要配置alapi_token，详见http://www.alapi.cn/api/view/93")
            return None
        url = "https://v2.alapi.cn/api/zaobao"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = f"token={alapi_token}&format=json"
        response = requests.request("POST", url, data=payload, headers=headers).json()
        if response.get("code", 404) == 200:
            return response.get("data", None)
        else:
            logger.error(f"[morning_news]Get morning_news fail, error code:{response.get('code')}, error msg:{response.get('msg', 'fail')}")
            return None

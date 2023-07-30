# encoding:utf-8

import plugins
from common.log import logger
from plugins import *


callback_dict = {}
def register(name):
  def decorator(func):
    callback_dict[name] = func
    return func
  return decorator

@plugins.register(
    name="dailynotify",
    desire_priority=1,
    hidden=True,
    desc="每日通知工具集合",
    version="0.1",
    author="SurfRid3r",
)
class dailynotify(Plugin):
    def __init__(self):
        super().__init__()
        curdir = os.path.dirname(__file__)
        config_path = os.path.join(curdir, "config.json")
        if not os.path.exists(config_path):
            logger.info("[Dailynotify]配置文件不存在，将使用config-template.json模板")
            config_path = os.path.join(curdir, "config-template.json")

        with open(config_path, mode="r", encoding="utf-8") as f:
            self.conf = json.load(f)

        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Dailynotify] inited")
    


    def on_handle_context(self, e_context: EventContext):
        for func_name, tool_conf in self.conf.items():
            if tool_conf.get("enable", False) and e_context["context"].content.startswith(tool_conf.get("command_prefix")):
                e_context = callback_dict[func_name](tool_conf, e_context)

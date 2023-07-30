# morning_news
[chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)的早报插件

- [x] `morning_news`: 通过[alapi 每日60秒早报](http://www.alapi.cn/api/view/93)实现，建议配合插件[timetask](https://github.com/haikerapples/timetask)食用。
- [x] `weather_notify`: 通过[qweather](https://console.qweather.com/#/console)接口查询天气，用于通知天气状态及是否要带雨伞。同样建议配合插件[timetask](https://github.com/haikerapples/timetask)

## 使用
### morning_news
该插件能够获取早报，支持图片形式或者文本形式推送。
1. 在目录下复制`config.json.template`为`config.json`，然后填写`alapi_token`，获取方式可见[https://admin.alapi.cn/](https://admin.alapi.cn/)。
2. 确认`command_prefix`触发文本，默认是匹配开头消息为`/早报`触发。
3. 填写`type`发送的方式:
    - text:发送文本
    - imag_url:发送图片
```json
{
    "morning_news": {
        "enable": true,
        "command_prefix": "/早报",
        "alapi_token": "xxx",
        "type": "text",
        "example": "/早报"
    }
}
```

### weather_notify
该插件能够获取24小时内天气或3天内天气进行推送，并且会判断异常天气（温度骤升/骤降和雨天带伞）提醒。
1. 在目录下复制`config.json.template`为`config.json`，然后填写`qweather_token`，获取方式可见[https://qweather.com](https://console.qweather.com/#/console)
2. 确认`command_prefix`触发文本，默认是匹配开头消息为`/早报`触发。
3. 该插件会解析content后的参数，如未填全则不足的会按位置补充默认数值(`北京 hourly 异常提醒`)：
    - 第一个参数为城市
    - 第二个参数可选：`hourly` 和 `daily`,分别对应获取24h天气和3天内天气。
    - 第三个参数可选: 不填写或者填写`alway_send`则不会过滤发送天气，填写其他内容会判断是上述异常天气才会推送，如下则是只有异常天气才会推送（可用于每日提醒）。
```json
{
    "weather_notify": {
        "enable": true,
        "command_prefix": "/天气",
        "qweather_token": "xxx",
        "example": "/天气 北京 hourly 异常提醒"
    }
}
```
# morning_news
[chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)的早报插件

通过[alapi 每日60秒早报](http://www.alapi.cn/api/view/93)实现，建议配合插件[timetask](https://github.com/haikerapples/timetask)食用。

## 使用
1. 在目录下复制`config.json.template`为`config.json`，然后填写`alapi_token`，获取方式可见[https://admin.alapi.cn/](https://admin.alapi.cn/)。
2. 确认`command_prefix`触发文本，默认是匹配开头消息为`/早报`触发。
2. 填写`type`发送的方式:
    - text:发送文本
    - imag_url:发送图片
```json
{
    "command_prefix": "/早报",
    "alapi_token": "xxxxx",
    "type": "text"
}
```

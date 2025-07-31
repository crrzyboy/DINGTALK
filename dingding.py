import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
from datetime import datetime, timedelta


class DingTalkReminder:
    def __init__(self, webhook, secret):
        """
        初始化钉钉机器人
        :param webhook: 钉钉机器人webhook地址
        :param secret: 钉钉机器人密钥
        """
        self.webhook = webhook
        self.secret = secret

    def get_signature(self):
        """生成签名"""
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def send_reminder(self, title, content, at_all=True):
        """
        发送提醒消息
        :param title: 消息标题
        :param content: 消息内容
        :param at_all: 是否@所有人
        """
        timestamp, sign = self.get_signature()
        url = f"{self.webhook}&timestamp={timestamp}&sign={sign}"

        headers = {
            "Content-Type": "application/json;charset=utf-8"
        }

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": content
            },
            "at": {
                "isAtAll": at_all
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if result.get("errcode") == 0:
                print("提醒消息发送成功！")
                return True
            else:
                print(f"消息发送失败: {result.get('errmsg')}")
                return False
        except Exception as e:
            print(f"发送消息时发生错误: {str(e)}")
            return False


def get_week_info():
    """获取当前周信息"""
    today = datetime.now()
    # 获取本周一日期
    monday = today - timedelta(days=today.weekday())
    # 获取本周五日期
    friday = monday + timedelta(days=4)

    return {
        "current_date": today.strftime("%Y年%m月%d日"),
        "week_range": f"{monday.strftime('%m月%d日')}-{friday.strftime('%m月%d日')}"
    }


def main():
    # 请替换为你的钉钉机器人webhook和secret
    WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=fb2a470f76886fffb4025ab38f3c8d53f5132f485986066892dc60875e08cb96"
    SECRET = "SEC977656c041d06d096e0f8c53c7b8a56e5e3d1e77d8042c0b8eb86a75db650755"

    reminder = DingTalkReminder(WEBHOOK, SECRET)
    week_info = get_week_info()

    # 构建提醒消息
    title = "工时表填写提醒"
    content = f"""
    # ⚠️ 工时表填写提醒

    各位同事，大家好！

    今天是 {week_info['current_date']}，本周({week_info['week_range']})的工时表填写工作即将截止。

    请大家尽快登录钉钉系统，完成本周工时表的填写与提交。

    📌 温馨提示：
    1. 请准确填写各项工作内容及耗时
    2. 确保工时表的完整性和准确性
    3. 请在规定时间前完成提交

    感谢大家的配合！

    @所有人
    """

    # 发送提醒
    reminder.send_reminder(title, content, at_all=True)


if __name__ == "__main__":
    main()

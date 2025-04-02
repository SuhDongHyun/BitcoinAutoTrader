from datetime import datetime
import requests

webhook_url = "https://discord.com/api/webhooks/1356959633691906149/NawO0vE9WOYZbQPhShQFinxSMTSNFArFB-8jXRZafZ5TQ0F_4zxGmEf5sRNht1-WRHXG"


def send_message(msg: str):
    now = datetime.now()
    content = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}]\n{msg}"}
    requests.post(webhook_url, data=content)

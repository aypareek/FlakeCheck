# flakecheck/notify_slack.py

import os
import requests

def send_slack_notification(message, webhook_url=None):
    webhook = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        print("⚠️ SLACK_WEBHOOK_URL not set. Skipping Slack notification.")
        return

    payload = {"text": message}
    try:
        response = requests.post(webhook, json=payload)
        if response.status_code != 200:
            print(f"Slack notification failed: {response.text}")
    except Exception as e:
        print(f"Error sending Slack message: {e}")

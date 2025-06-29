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


def send_slack_report(report_path="outputs/audit_report.md", webhook_url=None):
    webhook = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        print("⚠️ SLACK_WEBHOOK_URL not set. Skipping Slack report.")
        return

    try:
        with open(report_path, "r") as f:
            report_content = f.read()

        if len(report_content) > 3500:
            report_content = report_content[:3500] + "\n... (truncated)"

        payload = {"text": f"📄 *FlakeCheck Report Summary:*\n```{report_content}```"}
        response = requests.post(webhook, json=payload)

        if response.status_code != 200:
            print(f"Slack message failed: {response.text}")
    except Exception as e:
        print(f"Error sending report to Slack: {e}")

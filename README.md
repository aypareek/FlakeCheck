# ❄️ FlakeCheck

FlakeCheck is an open-source tool that audits your Snowflake data warehouse for performance and cost optimization.

It scans warehouse usage, queries, and storage metrics, then provides **actionable recommendations** and optionally sends a **Slack notification** when complete.

## 📊 Features
- Identify underused or oversized warehouses
- Detect long-running or costly queries
- Report on large or unused tables
- Suggest warehouse and query optimizations
- Generate markdown reports
- Optional Slack notifications

## 🚀 Quick Start
```bash
git clone https://github.com/aypareek/flakecheck.git
cd flakecheck
pip install -r requirements.txt
cp config.yaml.example config.yaml  # then edit with your Snowflake creds
python main.py
```

## 🔔 Slack Integration
Set your Slack Webhook as an environment variable:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

## 📄 License
[MIT](./LICENSE)

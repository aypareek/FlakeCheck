# ❄️ FlakeCheck

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CI Status](https://img.shields.io/github/actions/workflow/status/<your-username>/flakecheck/ci.yml?branch=main)

**FlakeCheck** is an open-source Snowflake audit and cost optimization toolkit built for data teams.

It analyzes your Snowflake usage, recommends improvements, and provides visual dashboards and Slack alerts — all with minimal setup.

---

## 🚀 Features

✅ Audit warehouse settings (auto-suspend, size, idle state)  
✅ Analyze query costs and performance  
✅ Identify large and inactive tables  
✅ Generate actionable recommendations  
✅ Send summary + report to Slack  
✅ Visualize usage trends in Streamlit (credits, storage, queries)  
✅ Configurable for Standard or Enterprise Snowflake accounts  
✅ Markdown + optional HTML/PDF reports  

---

## 📦 Installation

```bash
git clone https://github.com/<your-username>/flakecheck.git
cd flakecheck
pip install -r requirements.txt
cp config.yaml.example config.yaml
```

---

## 🔧 Configuration

Edit `config.yaml`:

```yaml
account_type: standard  # or enterprise

auth_method: externalbrowser

snowflake:
  account: your_account
  user: your_user
  warehouse: COMPUTE_WH
  database: YOUR_DB
  schema: PUBLIC

keypair:
  private_key_path: /path/to/key.pk8
  private_key_passphrase: your_pass
```

---

## 🧪 Run Audit

```bash
./run_flakecheck.sh
```

Check the output:

```bash
cat outputs/audit_report.md
```

---

## 📊 View Dashboard

```bash
./run_dashboard.sh
```

Includes:
- 💳 Credits used by warehouse
- 🧱 Storage by database
- 👤 Top users by query cost
- 📈 Query volume over time
- 📄 Markdown audit report

---

## 📬 Slack Integration

Set your Slack webhook (optional):

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

You’ll receive:
- ✅ Completion message
- 📄 Report summary in Slack

---

## 🤝 Contributing

Pull requests are welcome!  
Feature ideas? Open an issue or discussion.

---

## 📄 License

[MIT](LICENSE)

---

> Created by [@aypareek](https://github.com/aypareek)

# main.py
from flakecheck.check_warehouses import check_warehouses
from flakecheck.check_queries import check_queries
from flakecheck.check_storage import check_storage
from flakecheck.recommend_optimizer import generate_recommendations
from flakecheck.notify_slack import send_slack_notification
import datetime
import os

def main():
    print("🚀 Running FlakeCheck - Snowflake Health & Cost Auditor")

    warehouse_report = check_warehouses()
    query_report = check_queries()
    storage_report = check_storage()

    recommendations = generate_recommendations(warehouse_report, query_report, storage_report)

    report_md = f"# FlakeCheck Report - {datetime.datetime.now().strftime('%Y-%m-%d')}
"
    report_md += warehouse_report + "\n" + query_report + "\n" + storage_report + "\n"
    report_md += "## 🔧 Optimization Recommendations\n" + recommendations

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/audit_report.md", "w") as f:
        f.write(report_md)

    print("✅ Report generated at outputs/audit_report.md")

    send_slack_notification("FlakeCheck audit completed. Check the latest report.")

if __name__ == "__main__":
    main()

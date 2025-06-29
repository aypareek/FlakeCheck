# main.py

import argparse
import datetime
import os
import subprocess

from flakecheck.snowflake_connector import get_snowflake_connection, load_config
from flakecheck.check_warehouses import check_warehouses
from flakecheck.check_queries import check_queries
from flakecheck.check_storage import check_storage
from flakecheck.recommend_optimizer import generate_recommendations
from flakecheck.notify_slack import send_slack_notification

def parse_args():
    parser = argparse.ArgumentParser(description="FlakeCheck: Snowflake Audit Tool")
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    return parser.parse_args()

def main():
    args = parse_args()

    # Load connection and config
    conn, config = get_snowflake_connection(args.config)

    try:
        print("🔍 Running warehouse checks...")
        warehouse_report = check_warehouses(conn)

        print("💳 Running query analysis...")
        query_report = check_queries(conn)

        print("🧱 Running storage analysis...")
        storage_report = check_storage(conn, config)

        print("🧠 Generating recommendations...")
        recommendations = generate_recommendations(
            warehouse_report, query_report, storage_report
        )

        report_path = "outputs/audit_report.md"
        os.makedirs("outputs", exist_ok=True)

        with open(report_path, "w") as f:
            f.write(f"# ❄️ FlakeCheck Report - {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(warehouse_report)
            f.write(query_report)
            f.write(storage_report)
            f.write(recommendations)

        print(f"✅ Report generated at {report_path}")

        # Optional Slack Notification
        send_slack_notification("✅ FlakeCheck audit completed. Report is ready.")

    finally:
        conn.close()

    # Ask to launch Streamlit dashboard
    launch = input("📊 Would you like to open the Streamlit dashboard? (y/n): ").lower()
    if launch == 'y':
        subprocess.run(["streamlit", "run", "dashboard.py"])

if __name__ == "__main__":
    main()

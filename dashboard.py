# dashboard.py

import streamlit as st

def load_report(file_path="outputs/audit_report.md"):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No report found. Run FlakeCheck first."

def main():
    st.set_page_config(page_title="FlakeCheck Dashboard", layout="wide")
    st.title("❄️ FlakeCheck - Snowflake Audit Report")
    st.markdown("---")

    report = load_report()
    st.markdown(report, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

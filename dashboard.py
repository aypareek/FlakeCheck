# dashboard.py

import streamlit as st
import pandas as pd
import altair as alt
from flakecheck.snowflake_connector import get_snowflake_connection
from flakecheck.metrics_collector import (
    get_warehouse_credit_trends,
    get_storage_by_database,
    get_top_users_by_query_cost,
    get_query_count_over_time
)

def load_report(file_path="outputs/audit_report.md"):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No report found. Run FlakeCheck first."

def main():
    st.set_page_config(page_title="FlakeCheck Dashboard", layout="wide")
    st.title("❄️ FlakeCheck - Snowflake Audit Dashboard")
    st.markdown("---")

    config_path = st.sidebar.text_input("Config file path", "config.yaml")
    if st.sidebar.button("Load Usage Metrics"):
        conn, _ = get_snowflake_connection(config_path)
        with st.spinner("Fetching metrics..."):
            credits_df = get_warehouse_credit_trends(conn)
            storage_df = get_storage_by_database(conn)
            user_df = get_top_users_by_query_cost(conn)
            query_trend_df = get_query_count_over_time(conn)
            conn.close()

        if not credits_df.empty:
            st.subheader("💳 Credits Used by Warehouse (Last 60 Days)")
            chart = alt.Chart(credits_df).mark_line().encode(
                x='usage_date:T',
                y='total_credits:Q',
                color='warehouse_name:N'
            ).properties(width=800)
            st.altair_chart(chart, use_container_width=True)

        if not storage_df.empty:
            st.subheader("🧱 Storage by Database (GB)")
            bar = alt.Chart(storage_df).mark_bar().encode(
                x='total_gb:Q',
                y=alt.Y('database_name:N', sort='-x')
            ).properties(width=800)
            st.altair_chart(bar, use_container_width=True)

        if not user_df.empty:
            st.subheader("👤 Top Users by Query Credits (Last 30 Days)")
            bar = alt.Chart(user_df).mark_bar().encode(
                x='total_credits:Q',
                y=alt.Y('user_name:N', sort='-x')
            ).properties(width=800)
            st.altair_chart(bar, use_container_width=True)

        if not query_trend_df.empty:
            st.subheader("📈 Query Volume Over Time")
            line = alt.Chart(query_trend_df).mark_line().encode(
                x='query_date:T',
                y='query_count:Q'
            ).properties(width=800)
            st.altair_chart(line, use_container_width=True)

    st.markdown("---")
    st.subheader("📄 FlakeCheck Markdown Report")
    st.markdown(load_report(), unsafe_allow_html=True)

if __name__ == "__main__":
    main()

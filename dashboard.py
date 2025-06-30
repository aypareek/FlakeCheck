# dashboard.py

import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
from flakecheck.snowflake_connector import get_snowflake_connection
from flakecheck.metrics_collector import (
    get_warehouse_credit_trends,
    get_storage_by_database,
    get_top_users_by_query_cost,
    get_query_count_over_time,
    fetch_daily_credits,
    get_database_query_activity,
    get_top_expensive_queries,
)
from flakecheck.anomaly_detector import detect_cost_anomaly


def load_report(file_path="outputs/audit_report.md"):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No report found. Run FlakeCheck first."


def main():
    logo_path = "logo/FlakeCheckWbg.png"
    image = Image.open(logo_path)
    st.set_page_config(page_title="FlakeCheck Dashboard", layout="wide")
    st.image(image, width=200)
    st.title("FlakeCheck - Snowflake Audit Dashboard")

    config_path = st.sidebar.text_input("Config file path", "config.yaml")
    if st.sidebar.button("Load Usage Metrics"):
        conn, _ = get_snowflake_connection(config_path)
        with st.spinner("Fetching metrics..."):
            credits_df = get_warehouse_credit_trends(conn)
            storage_df = get_storage_by_database(conn)
            user_df = get_top_users_by_query_cost(conn)
            query_trend_df = get_query_count_over_time(conn)
            db_activity_df = get_database_query_activity(conn, days=30)
            query_df = get_top_expensive_queries(conn, days=30, limit=20)

            # ---- COST ANOMALY DETECTION ----
            st.markdown("---")
            st.subheader("🔎 Cost Anomaly Detection")
            try:
                daily_df = fetch_daily_credits(conn, days=30)
                history = daily_df["daily_credits"].tolist()
                anomaly_result = detect_cost_anomaly(history)
                st.write(anomaly_result)

                line_chart = (
                    alt.Chart(daily_df)
                    .mark_line(point=True)
                    .encode(x="usage_date:T", y="daily_credits:Q")
                    .properties(width=800)
                )
                st.altair_chart(line_chart, use_container_width=True)
            except Exception as e:
                st.error(f"Could not fetch cost anomaly data: {e}")
            st.markdown("---")

            conn.close()

        if not credits_df.empty:
            st.subheader("💳 Credits Used by Warehouse (Last 60 Days)")
            chart = (
                alt.Chart(credits_df)
                .mark_line()
                .encode(x="usage_date:T", y="total_credits:Q", color="warehouse_name:N")
                .properties(width=800)
            )
            st.altair_chart(chart, use_container_width=True)

        if not storage_df.empty:
            st.subheader("🧱 Storage by Database (GB)")
            bar = (
                alt.Chart(storage_df)
                .mark_bar()
                .encode(x="total_gb:Q", y=alt.Y("database_name:N", sort="-x"))
                .properties(width=800)
            )
            st.altair_chart(bar, use_container_width=True)

        if not user_df.empty:
            st.subheader("👤 Top Users by Query Credits (Last 30 Days)")
            bar = (
                alt.Chart(user_df)
                .mark_bar()
                .encode(x="total_credits:Q", y=alt.Y("user_name:N", sort="-x"))
                .properties(width=800)
            )
            st.altair_chart(bar, use_container_width=True)

        if not query_trend_df.empty:
            st.subheader("📈 Query Volume Over Time")
            line = (
                alt.Chart(query_trend_df)
                .mark_line()
                .encode(x="query_date:T", y="query_count:Q")
                .properties(width=800)
            )
            st.altair_chart(line, use_container_width=True)

        if not db_activity_df.empty:
            st.subheader("🔥 Query Activity by Database (Last 30 Days)")
            heatmap = (
                alt.Chart(db_activity_df)
                .mark_rect()
                .encode(
                    y=alt.Y("database_name:N", sort="-x"),
                    x=alt.X("query_count:Q"),
                    color=alt.Color(
                        "query_count:Q", scale=alt.Scale(scheme="redyellowgreen")
                    ),
                )
                .properties(width=700, height=350)
            )
            # Alternatively, bar chart (sometimes clearer):
            bar = (
                alt.Chart(db_activity_df)
                .mark_bar()
                .encode(
                    x="query_count:Q",
                    y=alt.Y("database_name:N", sort="-x"),
                    color=alt.Color(
                        "query_count:Q", scale=alt.Scale(scheme="redyellowgreen")
                    ),
                )
                .properties(width=800)
            )
            st.altair_chart(bar, use_container_width=True)

    st.markdown("---")
    st.subheader("📄 FlakeCheck Markdown Report")
    st.markdown(load_report(), unsafe_allow_html=True)


if __name__ == "__main__":
    main()

# flakecheck/metrics_collector.py

import pandas as pd

def get_warehouse_credit_trends(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                warehouse_name,
                DATE_TRUNC('day', start_time) AS usage_date,
                SUM(credits_used) AS total_credits
            FROM snowflake.account_usage.warehouse_metering_history
            WHERE start_time >= DATEADD(day, -60, CURRENT_DATE())
            GROUP BY 1, 2
            HAVING SUM(credits_used) > 0
            ORDER BY usage_date DESC, warehouse_name
        """)
        rows = cursor.fetchall()
        columns = [col[0].lower() for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        df['usage_date'] = pd.to_datetime(df['usage_date'])
        df['total_credits'] = pd.to_numeric(df['total_credits'])
        return df
    finally:
        cursor.close()

def get_storage_by_database(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                table_catalog AS database_name,
                SUM(active_bytes + time_travel_bytes + failsafe_bytes) / 1024 / 1024 / 1024 AS total_gb
            FROM information_schema.table_storage_metrics
            GROUP BY table_catalog
            ORDER BY total_gb DESC
        """)
        rows = cursor.fetchall()
        columns = [col[0].lower() for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        df['total_gb'] = pd.to_numeric(df['total_gb'])
        return df
    finally:
        cursor.close()

def get_top_users_by_query_cost(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                user_name,
                SUM(credits_used_cloud_services) AS total_credits
            FROM snowflake.account_usage.query_history
            WHERE start_time >= DATEADD(day, -30, CURRENT_DATE())
              AND execution_status = 'SUCCESS'
            GROUP BY user_name
            HAVING total_credits > 0
            ORDER BY total_credits DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
        columns = [col[0].lower() for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        df['total_credits'] = pd.to_numeric(df['total_credits'])
        return df
    finally:
        cursor.close()


def get_query_count_over_time(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                DATE_TRUNC('day', start_time) AS query_date,
                COUNT(*) AS query_count
            FROM snowflake.account_usage.query_history
            WHERE start_time >= DATEADD(day, -30, CURRENT_DATE())
            GROUP BY query_date
            ORDER BY query_date ASC
        """)
        rows = cursor.fetchall()
        columns = [col[0].lower() for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        df['query_date'] = pd.to_datetime(df['query_date'])
        df['query_count'] = pd.to_numeric(df['query_count'])
        return df
    finally:
        cursor.close()

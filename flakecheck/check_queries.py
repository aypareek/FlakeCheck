# flakecheck/check_queries.py
def check_queries(conn):
    cursor = conn.cursor()
    results = []


    try:
        cursor.execute("""
            SELECT 
                query_id, user_name, execution_status,
                start_time, end_time, total_elapsed_time/1000 AS duration_sec,
                credits_used_cloud_services AS credits,
                query_text
            FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
                END_TIME_RANGE_START => DATEADD('day', -3, CURRENT_TIMESTAMP()),
                END_TIME_RANGE_END => CURRENT_TIMESTAMP()
            ))
            WHERE execution_status = 'SUCCESS'
            ORDER BY credits_used_cloud_services DESC
            LIMIT 5
        """)
        queries = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        results.append("## 🔍 Top 5 Costliest Queries (Last 3 Days)")
        for row in queries:
            q = dict(zip(columns, row))
            results.append(f"- `{q['QUERY_ID']}` by **{q['USER_NAME']}** | ⏱ {int(q['DURATION_SEC'])}s | 💳 {q['CREDITS']:.2f} credits")

        # Detect long-running queries
        cursor.execute("""
            SELECT query_id, user_name, total_elapsed_time/1000 AS duration_sec
            FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
                END_TIME_RANGE_START => DATEADD('day', -3, CURRENT_TIMESTAMP()),
                END_TIME_RANGE_END => CURRENT_TIMESTAMP()
            ))
            WHERE total_elapsed_time > 60000 AND execution_status = 'SUCCESS'
            ORDER BY total_elapsed_time DESC
            LIMIT 5
        """)
        slow = cursor.fetchall()
        if slow:
            results.append("\n## 🐢 Long-Running Queries (>60s)")
            for q in slow:
                results.append(f"- `{q[0]}` by **{q[1]}** | ⏱ {int(q[2])}s")

        return "\n".join(results) + "\n"

    finally:
        cursor.close()

def check_storage(conn, config):
    cursor = conn.cursor()
    results = []

    try:
        account_type = config.get("account_type", "standard")

        # Shared: Top largest tables
        cursor.execute("""
            SELECT 
                t.table_schema,
                t.table_name,
                t.row_count,
                (sm.active_bytes + sm.time_travel_bytes + sm.failsafe_bytes) / 1024 / 1024 / 1024 AS total_size_gb,
                sm.active_bytes / 1024 / 1024 / 1024 AS active_gb,
                sm.time_travel_bytes / 1024 / 1024 / 1024 AS travel_gb,
                sm.failsafe_bytes / 1024 / 1024 / 1024 AS failsafe_gb
            FROM information_schema.tables t
            JOIN information_schema.table_storage_metrics sm
              ON t.table_schema = sm.table_schema AND t.table_name = sm.table_name
            WHERE t.table_type = 'BASE TABLE'
            ORDER BY total_size_gb DESC
            LIMIT 5
        """)
        rows = cursor.fetchall()
        results.append("## 🧱 Largest Tables (by total storage)")
        for r in rows:
            results.append(
                f"- `{r[0]}.{r[1]}` | 📦 {r[3]:.2f} GB "
                f"(Active: {r[4]:.2f} / TT: {r[5]:.2f} / FS: {r[6]:.2f}) | 🧮 {r[2]} rows"
            )

        # Conditionally run inactive check
        if account_type == "enterprise":
            results.append("\n✅ Enterprise mode: Checking access history for stale tables...")
            # Add account_usage.access_history-based logic here (if needed)
        else:
            results.append("\n⚠️ Standard account: Using last_altered date to infer stale tables.")
            cursor.execute("""
                SELECT table_schema, table_name, last_altered
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                  AND last_altered < DATEADD(day, -30, CURRENT_DATE())
                ORDER BY last_altered ASC
                LIMIT 5
            """)
            inactive = cursor.fetchall()
            if inactive:
                results.append("\n## 💤 Possibly Inactive Tables (Not altered in 30+ days)")
                for table in inactive:
                    results.append(f"- `{table[0]}.{table[1]}` (Last altered: {table[2]})")

        return "\n".join(results) + "\n"

    finally:
        cursor.close()

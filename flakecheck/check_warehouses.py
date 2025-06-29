def check_warehouses(conn):
    cursor = conn.cursor()
    results = []

    try:
        cursor.execute("SHOW WAREHOUSES")
        warehouses = cursor.fetchall()

        columns = [col[0] for col in cursor.description]

        for row in warehouses:
            wh = dict(zip(columns, row))
            name = wh["name"]
            size = wh["size"]
            state = wh["state"]
            auto_suspend = wh.get("auto_suspend")
            auto_resume = wh.get("auto_resume")
            running = wh["running"]

            if state == "STARTED" and running == 0:
                results.append(
                    f"⚠️ Warehouse **{name}** is running but has no queries."
                )
            if auto_suspend is None or auto_resume != "true":
                results.append(
                    f"⚠️ Warehouse **{name}** is missing recommended suspend/resume settings."
                )

        if not results:
            return "## ✅ Warehouse Check\nAll warehouses look good!\n"

        return "## 🏗️ Warehouse Check\n" + "\n".join(["- " + r for r in results]) + "\n"

    finally:
        cursor.close()

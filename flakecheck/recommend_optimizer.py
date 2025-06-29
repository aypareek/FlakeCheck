# flakecheck/recommend_optimizer.py


def generate_recommendations(warehouse_report, query_report, storage_report):
    recommendations = ["## 🧠 Optimization Recommendations"]

    # --- Warehouse Recommendations ---
    if "no queries" in warehouse_report.lower():
        recommendations.append(
            "- ⚠️ One or more warehouses are running without queries. Consider reducing size or enabling auto-suspend."
        )

    if "missing recommended suspend/resume" in warehouse_report.lower():
        recommendations.append(
            "- ⏸ Some warehouses lack auto-suspend/auto-resume settings. Enable these to reduce idle costs."
        )

    # --- Query Recommendations ---
    if "💳" in query_report:
        recommendations.append(
            "- 🔍 High-credit queries detected. Review and optimize them using Snowflake's Query Profiler (e.g., avoid cross joins, unnecessary sorts, SELECT *)."
        )

    if "Long-Running Queries" in query_report:
        recommendations.append(
            "- 🐢 Some queries are running longer than expected. Investigate indexing, filtering, or breaking them into smaller tasks."
        )

    # --- Storage Recommendations ---
    if "TT:" in storage_report or "FS:" in storage_report:
        recommendations.append(
            "- 📦 Tables with large Time Travel or Fail-safe footprints found. Consider lowering Time Travel duration or optimizing data retention."
        )

    if "Not altered in 30+ days" in storage_report:
        recommendations.append(
            "- 💤 Inactive tables detected. If these are no longer needed, consider archiving or dropping them to save on storage costs."
        )

    if len(recommendations) == 1:
        recommendations.append(
            "- ✅ No major issues detected. Your Snowflake setup looks healthy!"
        )

    return "\n".join(recommendations) + "\n"

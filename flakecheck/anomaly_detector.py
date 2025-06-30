import statistics
import re


def detect_cost_anomaly(credit_history, threshold=2.0):
    """
    Detects if today's usage is a statistical anomaly.
    :param credit_history: List of daily credits, oldest to newest.
    :param threshold: Number of stddevs over mean to consider an anomaly.
    """
    if len(credit_history) < 7:
        return "Not enough data for anomaly detection."

    *past, today = credit_history
    mean = statistics.mean(past)
    stddev = statistics.stdev(past)
    if stddev == 0:
        return "No anomaly: usage is flat (no variation)."

    if today > mean + threshold * stddev:
        return f"⚠️ Anomaly detected: Today's credit usage ({today:.2f}) is much higher than average ({mean:.2f})."
    else:
        return (
            f"No cost anomaly detected today. (Usage: {today:.2f}, Average: {mean:.2f})"
        )


def get_sql_recommendation(sql):
    recs = []
    if re.search(r"\bSELECT\s+\*\b", sql, re.IGNORECASE):
        recs.append("Avoid SELECT *")
    if not re.search(r"\bWHERE\b", sql, re.IGNORECASE):
        recs.append("Consider adding a WHERE clause")
    if re.search(r"\bJOIN\b", sql, re.IGNORECASE) and re.search(
        r"\bON\s+1\s*=\s*1\b", sql, re.IGNORECASE
    ):
        recs.append("Avoid cross joins")
    if not recs:
        return "Looks OK"
    return "; ".join(recs)

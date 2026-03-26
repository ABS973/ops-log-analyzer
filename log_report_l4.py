import json

level_counts   = {}
service_counts = {}
error_samples  = []
skipped        = 0

VALID_LEVELS = {"INFO", "WARN", "ERROR", "DEBUG", "CRITICAL"}

with open("clean_logs_l4.txt", "r", encoding="utf-8") as f:
    for raw_line in f:
        line = raw_line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4:
            skipped += 1
            continue
        ts, level, service, msg = parts
        if level not in VALID_LEVELS:
            skipped += 1
            continue
        level_counts[level] = level_counts.get(level, 0) + 1
        service_counts[service] = service_counts.get(service, 0) + 1
        if level == "ERROR" and len(error_samples) < 5:
            error_samples.append(line)

summary = {"level_counts": level_counts, "service_counts": service_counts}

with open("summary_l4.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
print("summary_l4.json written")

top_services = sorted(service_counts.items(), key=lambda x: x[1], reverse=True)[:5]
lines = ["INCIDENT MINI-REPORT", "=" * 40, ""]
for lvl in ("INFO", "WARN", "ERROR", "DEBUG", "CRITICAL"):
    if lvl in level_counts:
        lines.append(f"{lvl}: {level_counts[lvl]}")
lines.append("")
lines.append("Top services:")
for svc, count in top_services:
    lines.append(f"  {svc}: {count}")
lines.append("")
lines.append("Sample ERROR logs:")
for sample in error_samples:
    lines.append(f"  {sample}")
if skipped:
    lines.append("")
    lines.append(f"(Skipped {skipped} malformed / invalid lines)")

with open("incident_report_l4.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("incident_report_l4.txt written")

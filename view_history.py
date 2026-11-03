from database import get_scan_history

history = get_scan_history()

print("SCAN HISTORY")
print("=" * 60)

for file_path, scan_time, finding_count in history:
    print(f"File: {file_path}")
    print(f"Scanned: {scan_time}")
    print(f"Findings: {finding_count}")
    print("-" * 60)
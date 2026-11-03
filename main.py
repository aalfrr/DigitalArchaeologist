
from pathlib import Path
from database import (
    initialize_database,
    record_scan,
    has_file_changed,
    update_file_state,
    save_findings,
    get_all_findings
)
from scanner import scan_folder
from extractors import extract_text
from detectors import detect_actions, associate_dates
from ranking import rank_finding
from report import generate_report


def main():
    initialize_database()
    folder = Path(__file__).parent / "sample_documents"
    files = scan_folder(folder)

    all_findings = []

    print(f"Found {len(files)} supported files.\n")
    skipped_files = 0

    for file in files:
        if not has_file_changed(file):
            print(f"Unchanged, skipping: {file.name}")
            skipped_files += 1
            continue
        try:
            content = extract_text(file)
            findings = detect_actions(content)
            findings = associate_dates(findings)

            for finding in findings:
                finding["priority"] = rank_finding(finding, file)
                finding["filename"] = file.name

                all_findings.append(finding)

            record_scan(file, len(findings))
            save_findings(file, findings)

            findings.sort(
                key=lambda item: item["priority"]["score"],
                reverse=True
            )

            print(f"\n{'=' * 50}")
            print(f"FILE: {file.name}")
            print("=" * 50)

            if not findings:
                print("No actionable phrases detected.")
                continue

            for finding in findings:
                print(f"\nCategory: {finding['category']}")
                print(f"Phrase: {finding['phrase']}")
                print(f"Context: {finding['context']}")

                if finding["dates"]:
                    for item in finding["dates"]:
                        print(
                            f"Date: {item['original']} -> {item['date']}"
                        )
                else:
                    print("Date: Not specified")

                print(f"Priority score: {finding['priority']['score']}")

                for reason in finding["priority"]["reasons"]:
                    print(f"  - {reason}")
            
            update_file_state(file)

        except Exception as error:
            print(f"Could not process {file.name}: {error}")

    print(f"\nSkipped unchanged files: {skipped_files}")
    # Generate the report AFTER all files have been processed.
    output_path = (
        Path(__file__).parent
        / "reports"
        / "latest_report.html"
    )

    all_findings = get_all_findings()
    generate_report(all_findings, output_path)

    print(f"\nHTML report generated: {output_path}")


if __name__ == "__main__":
    main()

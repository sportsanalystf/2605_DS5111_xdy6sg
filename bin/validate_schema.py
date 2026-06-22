#!/usr/bin/env python3
"""
validate_schema.py - Consumer-driven contract validator.
Reads JSONL from stdin and verifies each record matches the required
enrichment schema (video_id, cleaned_text required; tech_terms,
book_names optional arrays of strings).
"""

import sys
import json


def validate_payload(line_num, payload):
    """Validate a single line of JSON data against the target API contract."""
    required_fields = ["video_id", "cleaned_text"]
    optional_fields = ["tech_terms", "book_names"]

    if not isinstance(payload, dict):
        print(f"\u274c [Row {line_num}] Schema Failure: Record is not a valid JSON Object.")
        return False

    for field in required_fields:
        if field not in payload:
            print(f"\u274c [Row {line_num}] Schema Failure: Missing mandatory key '{field}'.")
            return False

    if not isinstance(payload["video_id"], str) or not payload["video_id"].strip():
        print(f"\u274c [Row {line_num}] Type Failure: 'video_id' must be a non-empty STRING.")
        return False

    if not isinstance(payload["cleaned_text"], str):
        print(f"\u274c [Row {line_num}] Type Failure: 'cleaned_text' must be a STRING.")
        return False

    return _validate_optional_arrays(line_num, payload, optional_fields)


def _validate_optional_arrays(line_num, payload, optional_fields):
    """Validate optional array-of-string fields."""
    for field in optional_fields:
        if field in payload:
            if not isinstance(payload[field], list):
                print(f"\u274c [Row {line_num}] Type Failure: '{field}' must be an ARRAY.")
                return False
            if not all(isinstance(item, str) for item in payload[field]):
                print(f"\u274c [Row {line_num}] Type Failure: '{field}' must be STRINGS.")
                return False
    return True


def main():
    """Read JSONL rows from stdin and validate each against the schema contract."""
    print("\U0001f680 Starting pipeline data contract validation...")
    total_records = 0
    failed_records = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        total_records += 1
        try:
            data = json.loads(line)
            if not validate_payload(total_records, data):
                failed_records += 1
        except json.JSONDecodeError:
            print(f"\u274c [Row {total_records}] Syntax Failure: Line is not valid JSON Lines.")
            failed_records += 1

    print("\n--- Validation Summary ---")
    if total_records == 0:
        print("\u26a0\ufe0f Warning: No records were processed via stdin.")
        sys.exit(1)
    elif failed_records > 0:
        print(f"\U0001f534 Failure: {failed_records}/{total_records} records violated contract.")
        sys.exit(1)
    else:
        print(f"\U0001f7e2 Success: All {total_records} records match the required contract!")
        sys.exit(0)


if __name__ == '__main__':
    main()

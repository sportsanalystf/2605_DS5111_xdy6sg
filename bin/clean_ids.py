#!/usr/bin/env python3
"""
clean_ids.py - Filters valid YouTube IDs from stdin.
Logs invalid IDs to pipeline_autid.log with timestamps.
"""
import sys
import re
import logging

logging.basicConfig(
    filename='pipeline_autid.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def is_valid_youtube_id(candidate):
    """Return True if candidate is a valid 11-char YouTube ID."""
    valid_id_pattern = re.compile(r'^[A-Za-z0-9_-]{11}$')
    return bool(valid_id_pattern.match(candidate))

def main():
    """Read YouTube IDs from stdin, print valid ones, log invalid ones."""
    try:
        for line in sys.stdin:
            candidate = line.strip()
            if not candidate:
                continue
            if is_valid_youtube_id(candidate):
                print(candidate, flush=True)
            else:
                logging.warning("Invalid YouTube ID: '%s'", candidate)
    except KeyboardInterrupt:
        sys.stderr.write('\n')
        sys.exit(0)

if __name__ == '__main__':
    main()

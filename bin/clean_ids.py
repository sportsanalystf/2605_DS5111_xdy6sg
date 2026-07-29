#!/usr/bin/env python3

import sys
import re
import logging

logging.basicConfig(
    filename='pipeline_autid.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

VALID_ID_PATTERN = re.compile(r'^[A-Za-z0-9_-]{11}$')

def is_valid_youtube_id(candidate):
    return bool(VALID_ID_PATTERN.match(candidate))

def main():
    try:
        for line in sys.stdin:
            candidate = line.strip()
            if not candidate:
                continue
            if is_valid_youtube_id(candidate):
                print(candidate, flush=True)
            else:
                logging.warning(f"Invalid YouTube ID: '{candidate}'")
    except KeyboardInterrupt:
        sys.stderr.write('\n')
        sys.exit(0)

if __name__ == '__main__':
    main()

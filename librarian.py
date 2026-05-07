import os
import json
import datetime
import re

DOCS_DIR = "docs"
INDEX_FILE = os.path.join(DOCS_DIR, "00_INDEX.md")
ERROR_LOG = os.path.join(DOCS_DIR, "ERRORS", "ERROR_LOG.md")
CODING_RULES = os.path.join(DOCS_DIR, "PROTOCOL", "CODING_RULES.md")
CURRENT_MISSION = os.path.join(DOCS_DIR, "HANDOVER", "CURRENT_MISSION.md")

class Librarian:
    def __init__(self):
        if not os.path.exists(DOCS_DIR):
            os.makedirs(DOCS_DIR)

    def query(self, query_str):
        """Search all docs for a query string."""
        results = []
        for root, dirs, files in os.walk(DOCS_DIR):
            for file in files:
                if file.endswith(".md") and file != "00_INDEX.md":
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if query_str.lower() in line.lower():
                                results.append(f"{path} — Line {i+1}: {line.strip()}")
        
        if not results:
            return f"No results found for '{query_str}'."
        return "\n".join(results[:10]) # Return top 10

    def log_error(self, error_msg, fix_applied, file_affected):
        """Log a new error to ERROR_LOG.md."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        entry = f"""
---
DATE       : {timestamp}
FILE       : {file_affected}
ERROR      : {error_msg}
SYMPTOM    : [Not specified]
ROOT CAUSE : [To be determined]
FIX APPLIED: {fix_applied}
DO NOT     : [Not specified]
STATUS     : RESOLVED
---
"""
        with open(ERROR_LOG, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f" >> [LIBRARIAN] Error logged for {file_affected}.")
        self.update_index()

    def update_index(self):
        """Rebuilds 00_INDEX.md with metadata and summaries."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. Get Locked Files from CODING_RULES
        locked_files = "  - [No locked files found]"
        if os.path.exists(CODING_RULES):
            with open(CODING_RULES, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                match = re.search(r"LOCKED FILES.*?\n(.*?)(\n\n|#|$)", content, re.DOTALL | re.IGNORECASE)
                if match:
                    locked_files = match.group(1).strip()

        # 2. Get Last 5 Errors
        last_errors = "  - [No errors logged]"
        if os.path.exists(ERROR_LOG):
            with open(ERROR_LOG, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                entries = content.split("---")
                valid_entries = [e.strip() for e in entries if "DATE" in e]
                if valid_entries:
                    last_errors = "\n".join([f"  - {e[:200]}..." for e in valid_entries[-5:]][::-1])

        # 3. Get Current Mission Status
        mission_status = "  - [No mission status found]"
        if os.path.exists(CURRENT_MISSION):
            with open(CURRENT_MISSION, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                mission_status = "".join(lines[:10]).strip()

        index_content = f"""# SOVEREIGN PROJECT — MASTER INDEX
Last updated: {timestamp}

## QUICK LOOKUP
| I need to know...              | Go to                              |
|--------------------------------|------------------------------------|
| A past error and its fix       | ERRORS/ERROR_LOG.md                |
| What files NOT to touch        | PROTOCOL/CODING_RULES.md          |
| How to deploy / launch         | PROTOCOL/DEPLOY_PROTOCOL.md       |
| What each core file does       | ARCHITECTURE/SYSTEM_MAP.md        |
| Current mission / what to build| HANDOVER/CURRENT_MISSION.md       |
| How DNA/RL engine works        | ARCHITECTURE/DNA_ENGINE.md        |
| Telegram report rules          | ARCHITECTURE/TELEGRAM_PROTOCOL.md |
| What was completed before      | HANDOVER/DONE_LOG.md              |
| Open bugs / workarounds active | HANDOVER/KNOWN_ISSUES.md          |

## LOCKED FILES (do not edit without Commander approval)
{locked_files}

## LAST 5 ERRORS LOGGED
{last_errors}

## CURRENT MISSION STATUS
{mission_status}
"""
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(index_content)
        print(" >> [LIBRARIAN] 00_INDEX.md updated.")

    def guard_check(self, filename):
        """Checks if a file is marked as LOCKED."""
        if os.path.exists(CODING_RULES):
            with open(CODING_RULES, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()
                if filename.lower() in content and "locked" in content:
                    return "LOCKED"
        return "FREE"

if __name__ == "__main__":
    import argparse
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update the index")
    parser.add_argument("--query", type=str, help="Query the docs")
    parser.add_argument("--log", nargs=3, metavar=('MSG', 'FIX', 'FILE'), help="Log an error")
    args = parser.parse_args()

    lib = Librarian()
    if args.update:
        lib.update_index()
    elif args.query:
        print(lib.query(args.query))
    elif args.log:
        lib.log_error(args.log[0], args.log[1], args.log[2])
    else:
        lib.update_index()

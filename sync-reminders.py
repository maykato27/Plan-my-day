#!/usr/bin/env python3
"""Pull open items from the macOS Reminders "Inbox" list into markdown files."""

import subprocess
import os
from datetime import datetime

RAW_FILE = os.path.expanduser("~/context/admin/reminders-raw.md")
ORGANIZED_FILE = os.path.expanduser("~/context/admin/reminders-organized.md")

CATEGORIES = {
    "Job Search": [
        "apply", "application", "interview", "resume", "linkedin",
        "recruiter", "referral", "salary", "offer", "career", "hiring",
        "cover letter", "job", "role", "eucalyptus", "mitchell",
    ],
    "Health & IVF": [
        "ivf", "doctor", "appointment", "medication", "med", "clinic",
        "prescription", "blood", "hospital", "nurse", "cycle", "fertility",
        "injection", "retrieval", "transfer",
    ],
    "Personal": [
        "dog", "gym", "swim", "workout", "grocery", "groceries",
        "errand", "home", "house", "laundry", "clean", "pick up", "drop off",
        "buy", "store",
    ],
    "Finance": [
        "pay", "bill", "payment", "bank", "invoice", "rent",
        "subscription", "cancel", "renew", "charge",
        "401", "ira", "invest", "savings", "tax",
    ],
    "Learning": [
        "learn", "course", "read", "book", "study", "agentic",
        "tutorial", "research", "watch", "practice",
    ],
    "Admin": [
        "email", "call", "schedule", "meeting", "book", "confirm",
        "send", "reply", "message", "text", "follow up",
    ],
    "Quotes & Affirmations": [
        "quote", "affirmation", "mantra", "remind myself", "i am",
        "inspire", "motivation", "note to self",
    ],
}


def get_reminders():
    script = """
    tell application "Reminders"
        set inbox to list "Inbox"
        set openItems to (reminders of inbox whose completed is false)
        set output to ""
        repeat with r in openItems
            set output to output & name of r & linefeed
        end repeat
        return output
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"AppleScript error: {result.stderr.strip()}")
    return [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]


def categorize(reminders):
    buckets = {cat: [] for cat in CATEGORIES}
    buckets["Other"] = []
    for item in reminders:
        lower = item.lower()
        matched = False
        for cat, keywords in CATEGORIES.items():
            if any(kw in lower for kw in keywords):
                buckets[cat].append(item)
                matched = True
                break
        if not matched:
            buckets["Other"].append(item)
    return buckets


def write_raw(reminders, timestamp):
    with open(RAW_FILE, "w") as f:
        f.write(f"# Reminders — Inbox\n\n_Last synced: {timestamp}_\n\n")
        for item in reminders:
            f.write(f"- [ ] {item}\n")


def write_organized(buckets, timestamp):
    with open(ORGANIZED_FILE, "w") as f:
        f.write(f"# Reminders — Organized\n\n_Last synced: {timestamp}_\n\n")
        for cat, items in buckets.items():
            if items:
                f.write(f"## {cat}\n\n")
                for item in items:
                    f.write(f"- [ ] {item}\n")
                f.write("\n")


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    reminders = get_reminders()
    write_raw(reminders, timestamp)
    write_organized(categorize(reminders), timestamp)
    total = len(reminders)
    print(f"Synced {total} reminder{'s' if total != 1 else ''}.")
    print(f"  Raw:       {RAW_FILE}")
    print(f"  Organized: {ORGANIZED_FILE}")

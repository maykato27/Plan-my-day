# Plan My Day

A personal productivity system I built to eliminate the friction of daily planning. It connects my macOS Reminders, Google Calendar, and daily notes into a single workflow triggered by one prompt.

---

## The Problem

I was spending 20+ minutes every morning context-switching between my reminders app, calendar, and a blank notes page to piece together a plan for the day. Tasks were getting lost, energy patterns weren't being respected, and there was no single source of truth.

## What I Built

A lightweight personal OS that:
- **Pulls open tasks** from macOS Reminders and auto-categorizes them by topic (Job Search, Health, Finance, Learning, Admin)
- **Reads my Google Calendar** to surface existing commitments before scheduling
- **Generates a structured daily note** with a time-blocked schedule, running log, and end-of-day reflection template
- **Persists decisions** — completed reflections, carry-overs, and energy patterns feed back into future planning

One trigger ("plan my day") runs the full sequence.

## How It Works

```
macOS Reminders → sync-reminders.py → reminders-organized.md
                                              ↓
Google Calendar (gcalcli) ──────────→ daily schedule
                                              ↓
                                   daily-note YYYY-MM-DD.md
```

| Script | What it does |
|--------|-------------|
| `sync-reminders.py` | Fetches open Reminders via AppleScript, writes categorized markdown |
| `gcalcli.sh` | gcalcli wrapper for reading and writing Google Calendar events |
| `gcal-setup.py` | One-time OAuth setup for Google Calendar API |
| `templates/daily-note.md` | Structured template: schedule table, running log, reflection |

## Setup

```bash
cp .env.example .env
# Add your Google OAuth credentials to .env

python3 gcal-setup.py   # one-time browser auth
python3 sync-reminders.py
```

Requires: Python 3.10+, [gcalcli](https://github.com/insanum/gcalcli), macOS (for Reminders access)

## Why I Built This

I wanted to deeply understand agentic AI workflows — not just use them, but design and connect them. This project gave me hands-on experience with:

- **OAuth 2.0** and API authentication flows
- **AppleScript automation** for native macOS integrations
- **Prompt-driven workflows** using Claude as a planning layer
- **System design thinking** — how to connect discrete tools into a reliable, low-friction loop

It also became a daily driver. I use it every morning.

---

*Built by Mayumi Kato · [maykato@gmail.com](mailto:maykato@gmail.com)*

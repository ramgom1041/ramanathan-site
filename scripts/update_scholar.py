#!/usr/bin/env python3
"""Fetch Google Scholar metrics and write scholar.json (run by GitHub Actions).

Best-effort: Google Scholar has no public API and may rate-limit/CAPTCHA
requests from CI IPs. Every run ends in exactly one clearly logged outcome:

  SUCCESS      -- fresh metrics fetched, scholar.json written
  RATE-LIMITED -- Scholar blocked/CAPTCHA'd the request; previous data kept
  FAILED       -- any other error (network, parsing, ...); previous data kept

The script always exits 0 so a failed fetch never breaks the workflow or
overwrites the last good scholar.json.
"""
import json
import os
import sys
import datetime

AUTHOR_ID = "TmbVeDMAAAAJ"          # Dr. S. Ramanathan — Google Scholar user id
OUT = os.path.join(os.path.dirname(__file__), "..", "scholar.json")


def log(line):
    """Print to the job log and, when on GitHub Actions, the step summary."""
    print(line, flush=True)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        try:
            with open(summary, "a", encoding="utf-8") as f:
                f.write(line + "\n\n")
        except OSError:
            pass


def load_previous():
    try:
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def is_rate_limit(exc):
    """scholarly raises MaxTriesExceededException when Scholar blocks/CAPTCHAs."""
    name = type(exc).__name__
    text = str(exc).lower()
    return "maxtries" in name.lower() or "captcha" in text or "cannot fetch" in text


def fetch():
    from scholarly import scholarly
    author = scholarly.search_author_id(AUTHOR_ID)
    author = scholarly.fill(author, sections=["indices", "counts"])
    if not author or "citedby" not in author:
        raise ValueError("Scholar returned no citation data for author %s" % AUTHOR_ID)
    return author


def main():
    previous = load_previous()
    author = fetch()
    year = datetime.date.today().year
    data = {
        "citations":       author.get("citedby", 0),
        "citations_since": author.get("citedby5y", 0),
        "h_index":         author.get("hindex", 0),
        "h_index_since":   author.get("hindex5y", 0),
        "i10_index":       author.get("i10index", 0),
        "i10_index_since": author.get("i10index5y", 0),
        "since_year":      year - 5,
        "by_year":         {str(k): v for k, v in (author.get("cites_per_year") or {}).items()},
        "updated":         datetime.date.today().isoformat(),
    }
    if not data["by_year"] and previous.get("by_year"):
        # keep previous histogram if Scholar returned none
        data["by_year"] = previous["by_year"]
        log("NOTE: Scholar returned no per-year histogram; kept previous one.")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    log("SUCCESS: scholar.json updated — citations %s -> %s, h-index %s -> %s (as of %s)" % (
        previous.get("citations", "?"), data["citations"],
        previous.get("h_index", "?"), data["h_index"],
        data["updated"]))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if is_rate_limit(e):
            log("RATE-LIMITED: Google Scholar blocked the request from this runner; "
                "keeping existing scholar.json. (%s: %s)" % (type(e).__name__, e))
        else:
            log("FAILED: %s: %s — keeping existing scholar.json." % (type(e).__name__, e))
        # exit 0 on purpose: never fail the workflow or overwrite good data
        sys.exit(0)

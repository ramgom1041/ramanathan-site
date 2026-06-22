#!/usr/bin/env python3
"""Fetch Google Scholar metrics and write scholar.json (run by GitHub Actions).

Best-effort: Google Scholar has no public API and may rate-limit/CAPTCHA from
CI IPs. If the fetch fails, the existing scholar.json is left untouched so the
site keeps showing the last good values.
"""
import json, os, sys, datetime

AUTHOR_ID = "TmbVeDMAAAAJ"          # Dr. S. Ramanathan — Google Scholar user id
OUT = os.path.join(os.path.dirname(__file__), "..", "scholar.json")

def main():
    from scholarly import scholarly
    a = scholarly.search_author_id(AUTHOR_ID)
    a = scholarly.fill(a, sections=["indices", "counts"])
    yr = datetime.date.today().year
    data = {
        "citations":       a.get("citedby", 0),
        "citations_since": a.get("citedby5y", 0),
        "h_index":         a.get("hindex", 0),
        "h_index_since":   a.get("hindex5y", 0),
        "i10_index":       a.get("i10index", 0),
        "i10_index_since": a.get("i10index5y", 0),
        "since_year":      yr - 5,
        "by_year":         {str(k): v for k, v in (a.get("cites_per_year") or {}).items()},
        "updated":         datetime.date.today().isoformat(),
    }
    if not data["by_year"]:
        # keep previous histogram if Scholar returned none
        try:
            data["by_year"] = json.load(open(OUT))["by_year"]
        except Exception:
            pass
    json.dump(data, open(OUT, "w"), indent=2)
    print("wrote", OUT, data)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Scholar fetch failed (keeping existing scholar.json):", e, file=sys.stderr)
        sys.exit(0)   # do not fail the workflow / overwrite good data

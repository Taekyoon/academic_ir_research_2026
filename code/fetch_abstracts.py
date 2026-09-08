#!/usr/bin/env python3
"""Fetch PubMed titles and abstracts for the PMIDs referenced by the frozen samples.

WHY THIS SCRIPT EXISTS INSTEAD OF A DATA FILE. The CLEF eHealth TAR collection itself ships
only PMIDs - its topic files carry a title, a boolean query and a list of PMIDs, and no abstract
text. That is the convention this repository follows: PMIDs and expert labels are redistributed,
abstract text is fetched from PubMed by the person reproducing the run. It keeps the repository
free of publisher-copyrighted abstract text and makes the provenance of every abstract explicit.

The output is one JSON object per line with keys pmid, title, abstract. An empty abstract field
is normal and expected for a small share of records (about 7% of this sample); those rows are
judged on the title alone and the judging script records them as title_only so the effect can
be reported rather than hidden.

Usage
    python fetch_abstracts.py --pmids data/pmids.txt --out clef_abstracts.jsonl
    python fetch_abstracts.py --pmids data/pmids.txt --out clef_abstracts.jsonl \
        --email you@example.org

NCBI asks that automated callers identify themselves with a contact address and a tool name. The
tool name is set; the address is OPTIONAL and is supplied only by you, on the command line. This
script never reads an address from the environment and never embeds one.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
TOOL = "recall-denominator-study"
BATCH = 200


def fetch_batch(pmids, email=None, timeout=180, attempts=4):
    params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml", "tool": TOOL}
    if email:
        params["email"] = email
    url = EFETCH + "?" + urllib.parse.urlencode(params)
    last = None
    for i in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return ET.fromstring(resp.read())
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"efetch failed after {attempts} attempts: {last}")


def extract(article):
    """Title plus the abstract's labelled sections joined in document order. Structured
    abstracts keep their section labels because the judge sees the same text a screener would."""
    pmid = article.findtext(".//PMID")
    title = " ".join((article.findtext(".//ArticleTitle") or "").split())
    parts = []
    for node in article.findall(".//Abstract/AbstractText"):
        body = " ".join((node.text or "").split())
        if not body:
            continue
        label = node.get("Label")
        parts.append(f"{label}: {body}" if label else body)
    return pmid, title, " ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pmids", required=True, help="one PMID per line")
    ap.add_argument("--out", required=True)
    ap.add_argument("--email", default=None,
                    help="optional contact address sent to NCBI; supply your own or omit")
    ap.add_argument("--sleep", type=float, default=0.4)
    args = ap.parse_args()

    wanted = [ln.strip() for ln in open(args.pmids) if ln.strip()]
    have = set()
    if os.path.exists(args.out):
        with open(args.out) as fh:
            for ln in fh:
                if ln.strip():
                    try:
                        have.add(str(json.loads(ln)["pmid"]))
                    except Exception:
                        pass
    todo = [p for p in wanted if p not in have]
    print(f"wanted {len(wanted):,} | already present {len(have):,} | to fetch {len(todo):,}",
          flush=True)

    n_ok = n_noabs = 0
    with open(args.out, "a") as fh:
        for i in range(0, len(todo), BATCH):
            root = fetch_batch(todo[i:i + BATCH], args.email)
            for article in root.findall(".//PubmedArticle"):
                pmid, title, abstract = extract(article)
                if not pmid:
                    continue
                n_ok += 1
                n_noabs += not abstract
                fh.write(json.dumps({"pmid": pmid, "title": title,
                                     "abstract": abstract}) + "\n")
            fh.flush()
            print(f"  {min(i + BATCH, len(todo)):,}/{len(todo):,}", flush=True)
            time.sleep(args.sleep)

    got = have | {str(json.loads(ln)["pmid"]) for ln in open(args.out) if ln.strip()}
    absent = [p for p in wanted if p not in got]
    print(f"\nfetched {n_ok:,} | no abstract body {n_noabs:,} "
          f"({n_noabs / max(n_ok, 1):.1%}) | still absent {len(absent):,}", flush=True)
    if absent:
        print(f"  absent PMIDs (records withdrawn or not in PubMed): {absent[:20]}", flush=True)


if __name__ == "__main__":
    main()

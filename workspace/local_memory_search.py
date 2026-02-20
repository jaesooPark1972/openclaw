import argparse
import glob
import os
import re
from collections import Counter

ROOT = r"C:\Users\JayPark1004\.openclaw\workspace"
TARGETS = [
    os.path.join(ROOT, "MEMORY.md"),
    os.path.join(ROOT, "memory", "*.md"),
]


def tokenize(text: str):
    text = text.lower()
    text = re.sub(r"[^\w\s가-힣]", " ", text)
    return [t for t in text.split() if len(t) > 1]


def read_targets():
    paths = []
    for t in TARGETS:
        if "*" in t:
            paths.extend(glob.glob(t))
        elif os.path.exists(t):
            paths.append(t)
    docs = []
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                docs.append((p, f.read()))
        except Exception:
            continue
    return docs


def score_doc(query_tokens, doc_text):
    tokens = tokenize(doc_text)
    if not tokens:
        return 0.0
    c = Counter(tokens)
    return sum(c[t] for t in query_tokens) / (len(tokens) ** 0.5)


def best_lines(query_tokens, doc_text, topn=3):
    lines = [ln.strip() for ln in doc_text.splitlines() if ln.strip()]
    scored = []
    for i, line in enumerate(lines, start=1):
        s = score_doc(query_tokens, line)
        if s > 0:
            scored.append((s, i, line))
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:topn]


def main():
    ap = argparse.ArgumentParser(description="Local fallback memory search (no OpenAI)")
    ap.add_argument("query", help="query text")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    q_tokens = tokenize(args.query)
    docs = read_targets()

    ranked = []
    for path, text in docs:
        s = score_doc(q_tokens, text)
        if s > 0:
            ranked.append((s, path, text))

    ranked.sort(reverse=True, key=lambda x: x[0])
    ranked = ranked[: args.top]

    if not ranked:
        print("NO_MATCH")
        return

    for idx, (score, path, text) in enumerate(ranked, start=1):
        print(f"[{idx}] score={score:.3f} path={path}")
        for _, line_no, line in best_lines(q_tokens, text, topn=2):
            print(f"  - L{line_no}: {line}")


if __name__ == "__main__":
    main()

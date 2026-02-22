import os, csv, json, datetime

ROOT = r"E:\문서"
STATE_PATH = r"C:\Users\JayPark1004\.openclaw\workspace\docs_review_state.json"
OUT_DIR = r"C:\Users\JayPark1004\.openclaw\workspace"
BATCH_SIZE = 1000


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"offset": 0, "batch": 0}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def collect_files(root):
    rows = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            try:
                st = os.stat(p)
            except Exception:
                continue
            rows.append((st.st_mtime, p, os.path.splitext(fn)[1].lower(), st.st_size))
    rows.sort(reverse=True, key=lambda x: x[0])
    return rows


def main():
    state = load_state()
    files = collect_files(ROOT)
    offset = state["offset"]
    batch_no = state["batch"] + 1
    chunk = files[offset:offset + BATCH_SIZE]

    out = os.path.join(OUT_DIR, f"docs_review_batch_{batch_no:03d}.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["FullName", "Extension", "Length", "LastWriteTime"])
        for mtime, path, ext, size in chunk:
            w.writerow([path, ext, size, datetime.datetime.fromtimestamp(mtime).isoformat()])

    state["offset"] = offset + len(chunk)
    state["batch"] = batch_no
    save_state(state)

    print(out)
    print(f"BATCH={batch_no}")
    print(f"COUNT={len(chunk)}")
    print(f"NEXT_OFFSET={state['offset']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = Path(__file__).resolve().parent / "weights-raw.txt"
PATTERN = re.compile(r"^(\d{4})年(\d{1,2})月(\d{1,2})日:\s*([\d.]+)\s*kg$")

def parse_records():
    records = {}
    failed = []
    for line in RAW_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        m = PATTERN.match(line)
        if not m:
            failed.append(line)
            continue
        y, mo, d, w = m.groups()
        date = f"{y}-{int(mo):02d}-{int(d):02d}"
        records[date] = {"weight": float(w), "bodyFat": None, "meals": []}
    if failed:
        raise ValueError("Parse failed:\n" + "\n".join(failed))
    return records

def main():
    records = parse_records()
    count = len(records)

    import_data = {
        "settings": {
            "height": None,
            "startWeight": None,
            "targetWeight": None,
            "targetBodyFat": None,
            "targetDate": None,
            "dailyCalGoal": 2000,
        },
        "records": records,
    }

    json_path = ROOT / "weight-import.json"
    json_path.write_text(json.dumps(import_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON: {count} records -> {json_path}")

    bundle_path = ROOT / "weight-bundle.js"
    bundle_path.write_text(
        "window.WEIGHT_IMPORT_RECORDS = " + json.dumps(records, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"Bundle: {count} records -> {bundle_path}")

    records_js = json.dumps(records, ensure_ascii=False)
    html_path = ROOT / "import-weights.html"
    html_path.write_text(
        HTML_TEMPLATE.replace("%%COUNT%%", str(count)).replace("%%RECORDS%%", records_js),
        encoding="utf-8",
    )
    print(f"HTML -> {html_path}")

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>体重データインポート</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 2rem auto; padding: 1rem; }
    button { padding: 0.75rem 1.5rem; font-size: 1rem; cursor: pointer; margin: 0.5rem 0.5rem 0.5rem 0; }
    .success { color: #059669; }
    .error { color: #dc2626; }
  </style>
</head>
<body>
  <h1>体重データインポート</h1>
  <p>localStorage に体重データをマージします（%%COUNT%%件）。</p>
  <p><strong>注意:</strong> 同じ日付は体重のみ上書き（食事データは保持）。</p>
  <button id="mergeBtn">既存データとマージしてインポート</button>
  <button id="replaceBtn">records を全置換してインポート</button>
  <div id="result"></div>
  <script>
    const STORAGE_KEY = "weightTrackerData_v1";
    const DEFAULT_DATA = {
      settings: { height: null, startWeight: null, targetWeight: null, targetBodyFat: null, targetDate: null, dailyCalGoal: 2000 },
      records: {}
    };
    const newRecords = %%RECORDS%%;

    function loadData() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return structuredClone(DEFAULT_DATA);
        const parsed = JSON.parse(raw);
        return {
          settings: { ...DEFAULT_DATA.settings, ...(parsed.settings || {}) },
          records: parsed.records || {}
        };
      } catch (e) {
        return structuredClone(DEFAULT_DATA);
      }
    }

    function mergeRecords(existing, incoming) {
      const merged = { ...existing };
      let added = 0, updated = 0;
      for (const [date, rec] of Object.entries(incoming)) {
        if (merged[date]) {
          merged[date] = { ...merged[date], weight: rec.weight, bodyFat: merged[date].bodyFat ?? rec.bodyFat };
          updated++;
        } else {
          merged[date] = rec;
          added++;
        }
      }
      return { merged, added, updated };
    }

    function doImport(replace) {
      const result = document.getElementById("result");
      try {
        let state = loadData();
        if (replace) {
          state.records = newRecords;
          localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
          result.innerHTML = '<p class="success">完了: ' + Object.keys(newRecords).length + '件（records置換）</p>';
        } else {
          const { merged, added, updated } = mergeRecords(state.records, newRecords);
          state.records = merged;
          localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
          result.innerHTML = '<p class="success">マージ完了: 新規 ' + added + '件, 更新 ' + updated + '件</p>';
        }
        result.innerHTML += '<p><a href="index.html">アプリを開く</a></p>';
      } catch (e) {
        result.innerHTML = '<p class="error">エラー: ' + e.message + '</p>';
      }
    }

    document.getElementById("mergeBtn").addEventListener("click", () => doImport(false));
    document.getElementById("replaceBtn").addEventListener("click", () => {
      if (confirm("既存のrecordsを全て置き換えます。settingsは保持されます。続行しますか？")) doImport(true);
    });
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    main()

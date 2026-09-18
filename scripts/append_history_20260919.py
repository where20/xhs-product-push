#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""append_history_20260919.py
追加 9/19 entry 到 history.json (按 cron task 步骤 11)
"""
import json
from pathlib import Path
from datetime import datetime

HIST = Path('/Users/xiaoan/WorkBuddy/xhs-product-push/history/history.json')
TODAY = '2026-09-19'

with open(HIST, 'r', encoding='utf-8') as f:
    entries = json.load(f)

# 9/19 entry (按 cron task step 11 格式)
new_entry = {
    'date': TODAY,
    'totalRuns': len(entries) + 1,
    'productCount': 5,
    'updateTime': f'{TODAY} 07:30',
    'status': '运行中'
}
entries.append(new_entry)

with open(HIST, 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print(f"✅ history.json 已追加 entry: {new_entry}")
print(f"   当前 entries: {len(entries)}")

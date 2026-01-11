#!/usr/bin/env python
"""
キーワードマッチングのテスト（pdfplumberなし）
"""

import re
from typing import Optional


def extract_value(text: str, keyword: str, pattern_type: str = 'standard') -> Optional[int]:
    """
    テキストから特定項目の数値を抽出
    """
    patterns = []

    if pattern_type == 'standard':
        # "項目名 金額" のパターン
        patterns.append(rf'{re.escape(keyword)}\s+([\d,]+)')
        patterns.append(rf'{re.escape(keyword)}[　\s]+([\d,]+)')

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return int(match.group(1).replace(',', ''))
            except ValueError:
                continue

    return None


# テストケース: スペース入りの「現 金 及 び 預 金」
test_cases = [
    # (テキスト, キーワード, 期待値)
    ('現 金 及 び 預 金 5,000,123', '現 金 及 び 預 金', 5000123),
    ('現金及び預金 5,000,123', '現金及び預金', 5000123),
    ('現金預金 5,000,123', '現金預金', 5000123),
    ('現 金 及 び 預 金　1,234,567', '現 金 及 び 預 金', 1234567),  # 全角スペース
]

print("=" * 70)
print("PDF解析キーワードマッチングテスト")
print("=" * 70)

all_passed = True

for text, keyword, expected in test_cases:
    result = extract_value(text, keyword)
    passed = result == expected
    all_passed = all_passed and passed

    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: '{text}'")
    print(f"       キーワード: '{keyword}' -> 結果: {result} (期待値: {expected})")

print("=" * 70)
if all_passed:
    print("✓ すべてのテストが成功しました")
else:
    print("✗ 一部のテストが失敗しました")
print("=" * 70)

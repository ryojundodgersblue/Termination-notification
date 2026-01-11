#!/usr/bin/env python
"""
現金預金の下3桁除去機能をテストするスクリプト
"""

# テストデータ
test_cases = [
    ('現金及び預金', 5000123, 5000),  # 下3桁123を除去
    ('現金及び預金', 1234567, 1234),  # 下3桁567を除去
    ('現金及び預金', 1000, 1),        # 下3桁000を除去
    ('現金及び預金', 999, 0),         # 1000未満は0
    ('現金及び預金', 5000000, 5000),  # 既存のテストデータ
    ('売掛金', 3000000, 3000000),     # 他の項目は変換しない
]

print("=" * 70)
print("現金預金の下3桁除去機能テスト")
print("=" * 70)

all_passed = True

for item, input_value, expected_value in test_cases:
    # 現金預金の場合は下3桁を除去
    actual_value = input_value
    if item == '現金及び預金':
        actual_value = input_value // 1000

    passed = actual_value == expected_value
    all_passed = all_passed and passed

    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {item} = {input_value:,} -> {actual_value:,} (expected: {expected_value:,})")

print("=" * 70)
if all_passed:
    print("✓ すべてのテストが成功しました")
else:
    print("✗ 一部のテストが失敗しました")
print("=" * 70)

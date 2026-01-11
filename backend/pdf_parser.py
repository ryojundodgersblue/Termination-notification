"""
PDF解析モジュール
決算報告書PDFから財務データを抽出します
"""

import re
import pdfplumber
from typing import Dict, Any, Optional, List


def extract_value(text: str, keyword: str, pattern_type: str = 'standard') -> Optional[int]:
    """
    テキストから特定項目の数値を抽出

    Args:
        text: 検索対象テキスト
        keyword: 検索キーワード
        pattern_type: パターンタイプ ('standard', 'with_unit', 'flexible')

    Returns:
        抽出した数値（整数）、見つからない場合はNone
    """
    # パターンバリエーション
    patterns = []

    if pattern_type == 'standard':
        # "項目名 金額" のパターン
        patterns.append(rf'{re.escape(keyword)}\s+([\d,]+)')
        patterns.append(rf'{re.escape(keyword)}[　\s]+([\d,]+)')

    elif pattern_type == 'with_unit':
        # "項目名 金額円" のパターン
        patterns.append(rf'{re.escape(keyword)}\s+([\d,]+)円?')
        patterns.append(rf'{re.escape(keyword)}[　\s]+([\d,]+)円?')

    elif pattern_type == 'flexible':
        # より柔軟なパターン（改行やスペースを許容）
        patterns.append(rf'{re.escape(keyword)}[　\s\n]+([\d,]+)')

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return int(match.group(1).replace(',', ''))
            except ValueError:
                continue

    return None


def extract_table_value(tables: List[List[List]], row_keyword: str, col_index: int = 1) -> Optional[int]:
    """
    テーブルから特定行の値を抽出

    Args:
        tables: pdfplumberで抽出したテーブルリスト
        row_keyword: 行のキーワード
        col_index: 列インデックス（デフォルト1 = 2列目）

    Returns:
        抽出した数値、見つからない場合はNone
    """
    for table in tables:
        for row in table:
            if row and len(row) > 0:
                # 最初のセルにキーワードが含まれているか確認
                if row[0] and row_keyword in str(row[0]):
                    if len(row) > col_index and row[col_index]:
                        # 数値抽出
                        value_str = str(row[col_index]).replace(',', '').replace('円', '').strip()
                        try:
                            return int(value_str)
                        except ValueError:
                            continue
    return None


def extract_balance_sheet(pdf_path: str) -> Dict[str, Any]:
    """
    貸借対照表からデータ抽出

    Args:
        pdf_path: PDFファイルパス

    Returns:
        抽出データの辞書
    """
    data = {
        'assets': {},  # 資産の部
        'liabilities': {},  # 負債の部
        'equity': {}  # 純資産の部
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            # 貸借対照表は通常2-3ページ目
            for page_num in range(min(len(pdf.pages), 5)):  # 最初の5ページをチェック
                page = pdf.pages[page_num]
                text = page.extract_text()

                # ページに「貸借対照表」が含まれているか確認
                if '貸借対照表' not in text:
                    continue

                tables = page.extract_tables()

                # 資産の部
                assets_keywords = {
                    '現金及び預金': ['現金及び預金', '現金預金'],
                    '売掛金': ['売掛金', '完成工事未収入金'],
                    '未成工事支出金': ['未成工事支出金'],
                    '材料貯蔵品': ['材料貯蔵品', '貯蔵品'],
                    '建物': ['建物'],
                    '構築物': ['構築物'],
                    '機械装置': ['機械装置', '機械及び装置'],
                    '車両運搬具': ['車両運搬具'],
                    'ソフトウェア': ['ソフトウェア', 'ソフトウエア'],
                    '出資金': ['出資金'],
                }

                for key, keywords in assets_keywords.items():
                    for keyword in keywords:
                        value = extract_value(text, keyword)
                        if value is not None:
                            data['assets'][key] = value
                            break

                # 負債の部
                liabilities_keywords = {
                    '工事未払金': ['工事未払金', '買掛金'],
                    '未払金': ['未払金'],
                    '未払法人税等': ['未払法人税等', '未払法人税'],
                    '未払消費税等': ['未払消費税等', '未払消費税'],
                    '未成工事受入金': ['未成工事受入金'],
                    '預り金': ['預り金', '預かり金'],
                    '長期借入金': ['長期借入金'],
                    '役員等借入金': ['役員借入金', '役員等借入金'],
                }

                for key, keywords in liabilities_keywords.items():
                    for keyword in keywords:
                        value = extract_value(text, keyword)
                        if value is not None:
                            data['liabilities'][key] = value
                            break

                # 純資産の部
                equity_keywords = {
                    '資本金': ['資本金'],
                    '繰越利益剰余金': ['繰越利益剰余金', '利益剰余金'],
                }

                for key, keywords in equity_keywords.items():
                    for keyword in keywords:
                        value = extract_value(text, keyword)
                        if value is not None:
                            data['equity'][key] = value
                            break

    except Exception as e:
        print(f"貸借対照表の抽出エラー: {str(e)}")

    return data


def extract_income_statement(pdf_path: str) -> Dict[str, Any]:
    """
    損益計算書からデータ抽出

    Args:
        pdf_path: PDFファイルパス

    Returns:
        抽出データの辞書
    """
    data = {
        'revenue': {},  # 売上
        'cost': {},  # 原価
        'expenses': {},  # 販売費及び一般管理費
        'non_operating': {}  # 営業外損益
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(min(len(pdf.pages), 8)):
                page = pdf.pages[page_num]
                text = page.extract_text()

                # ページに「損益計算書」が含まれているか確認
                if '損益計算書' not in text:
                    continue

                # 売上・原価
                revenue_keywords = {
                    '完成工事高': ['完成工事高', '売上高'],
                    '完成工事原価': ['完成工事原価', '売上原価'],
                }

                for key, keywords in revenue_keywords.items():
                    for keyword in keywords:
                        value = extract_value(text, keyword)
                        if value is not None:
                            data['revenue'][key] = value
                            break

                # 販売費及び一般管理費
                expense_keywords = {
                    '役員報酬': ['役員報酬'],
                    '給与手当': ['給与手当', '従業員給料手当'],
                    '法定福利費': ['法定福利費'],
                    '外注費': ['外注費'],
                    '旅費交通費': ['旅費交通費', '通信交通費'],
                    '通信費': ['通信費'],
                    '交際費': ['交際費'],
                    '減価償却費': ['減価償却費'],
                    '賃借料': ['賃借料'],
                }

                for key, keywords in expense_keywords.items():
                    for keyword in keywords:
                        value = extract_value(text, keyword)
                        if value is not None:
                            data['expenses'][key] = value
                            break

                # 営業外損益
                non_operating_keywords = {
                    '受取利息': ['受取利息', '受取利息及び配当金'],
                    '受取配当金': ['受取配当金'],
                    '雑収入': ['雑収入', 'その他営業外収益'],
                    '支払利息': ['支払利息'],
                }

                for key, keywords in non_operating_keywords.items():
                    for keyword in keywords:
                        value = extract_value(text, keyword)
                        if value is not None:
                            data['non_operating'][key] = value
                            break

    except Exception as e:
        print(f"損益計算書の抽出エラー: {str(e)}")

    return data


def extract_cost_report(pdf_path: str) -> Dict[str, Any]:
    """
    完成工事原価報告書からデータ抽出

    Args:
        pdf_path: PDFファイルパス

    Returns:
        抽出データの辞書
    """
    data = {}

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(min(len(pdf.pages), 8)):
                page = pdf.pages[page_num]
                text = page.extract_text()

                # ページに「完成工事原価報告書」が含まれているか確認
                if '完成工事原価報告書' not in text and '原価報告書' not in text:
                    continue

                keywords = {
                    '材料費': ['材料費'],
                    '労務費': ['労務費'],
                    '外注加工費': ['外注加工費', '外注費'],
                    '経費': ['経費'],
                }

                for key, keyword_list in keywords.items():
                    for keyword in keyword_list:
                        value = extract_value(text, keyword)
                        if value is not None:
                            data[key] = value
                            break

    except Exception as e:
        print(f"完成工事原価報告書の抽出エラー: {str(e)}")

    return data


def extract_equity_statement(pdf_path: str) -> Dict[str, Any]:
    """
    株主資本等変動計算書からデータ抽出

    Args:
        pdf_path: PDFファイルパス

    Returns:
        抽出データの辞書
    """
    data = {}

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(min(len(pdf.pages), 10)):
                page = pdf.pages[page_num]
                text = page.extract_text()

                # ページに「株主資本等変動計算書」が含まれているか確認
                if '株主資本等変動計算書' not in text and '資本等変動計算書' not in text:
                    continue

                keywords = {
                    '当期首残高_資本金': ['当期首残高.*資本金'],
                    '当期首残高_繰越利益剰余金': ['当期首残高.*繰越利益剰余金'],
                    '当期純利益': ['当期純利益'],
                    '当期末残高_資本金': ['当期末残高.*資本金'],
                    '当期末残高_繰越利益剰余金': ['当期末残高.*繰越利益剰余金'],
                }

                for key, keyword_list in keywords.items():
                    for keyword in keyword_list:
                        value = extract_value(text, keyword, pattern_type='flexible')
                        if value is not None:
                            data[key] = value
                            break

    except Exception as e:
        print(f"株主資本等変動計算書の抽出エラー: {str(e)}")

    return data


def parse_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    PDFから全データを抽出するメイン関数

    Args:
        pdf_path: PDFファイルパス

    Returns:
        抽出した全データを含む辞書
    """
    print(f"PDF解析開始: {pdf_path}")

    result = {
        'balance_sheet_assets': {},
        'balance_sheet_liabilities': {},
        'balance_sheet_equity': {},
        'income_statement': {},
        'non_operating': {},
        'cost_report': {},
        'equity_change': {}
    }

    # 貸借対照表
    balance_sheet_data = extract_balance_sheet(pdf_path)
    result['balance_sheet_assets'] = balance_sheet_data.get('assets', {})
    result['balance_sheet_liabilities'] = balance_sheet_data.get('liabilities', {})
    result['balance_sheet_equity'] = balance_sheet_data.get('equity', {})

    # 損益計算書
    income_data = extract_income_statement(pdf_path)
    result['income_statement'] = {**income_data.get('revenue', {}), **income_data.get('expenses', {})}
    result['non_operating'] = income_data.get('non_operating', {})

    # 完成工事原価報告書
    result['cost_report'] = extract_cost_report(pdf_path)

    # 株主資本等変動計算書
    result['equity_change'] = extract_equity_statement(pdf_path)

    print(f"✓ PDF解析完了")
    print(f"  抽出データ数: 資産 {len(result['balance_sheet_assets'])}件, "
          f"負債 {len(result['balance_sheet_liabilities'])}件, "
          f"損益 {len(result['income_statement'])}件")

    return result

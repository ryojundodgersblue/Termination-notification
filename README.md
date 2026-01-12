# 決算報告書 PDF→Excel 自動変換システム

建設業の決算報告書PDF（貸借対照表、損益計算書、完成工事原価報告書、株主資本等変動計算書）から数値を抽出し、所定のExcelテンプレートに自動入力するWebアプリケーションです。

## 機能概要

- ✅ PDFファイルのアップロード（ドラッグ&ドロップ対応）
- ✅ 財務データの自動抽出
  - 貸借対照表（資産・負債・純資産）
  - 損益計算書（売上・費用・営業外損益）
  - 完成工事原価報告書
  - 株主資本等変動計算書
- ✅ 抽出データをExcelテンプレートに自動書き込み
- ✅ 書式・マージセルを完全保持
- ✅ ワンクリックでExcelファイルをダウンロード

## 技術スタック

### フロントエンド
- React 18.2
- Vite 5.0
- TailwindCSS 3.3
- Axios 1.6
- **デプロイ先**: Vercel

### バックエンド
- Python 3.9+
- FastAPI 0.104
- pdfplumber 0.10 (PDF解析)
- openpyxl 3.1 (Excel操作)
- uvicorn 0.24 (ASGIサーバー)
- **デプロイ先**: Render

## 🚀 デプロイ方法

本番環境へのデプロイ手順については、以下のドキュメントを参照してください：

- 📖 **[DEPLOYMENT.md](./DEPLOYMENT.md)** - VercelとRenderへのデプロイ手順
- 🔧 **[ENV_SETUP_GUIDE.md](./ENV_SETUP_GUIDE.md)** - 環境変数の詳細な設定ガイド

### デプロイ構成

- **フロントエンド**: Vercel（無料枠あり、自動デプロイ）
- **バックエンド**: Render（無料枠あり、Pythonサポート良好）

### 環境変数（重要）

デプロイ時には以下の環境変数を正しく設定してください：

**Vercel（フロントエンド）**:
```
VITE_API_URL=https://your-backend.onrender.com/api/convert
```
⚠️ **必ず `/api/convert` まで含めてください**

**Render（バックエンド）**:
```
FRONTEND_URL=https://your-frontend.vercel.app
```
⚠️ **必ず `https://` を含めてください**

## プロジェクト構造

```
pdf-to-excel-converter/
├── backend/
│   ├── main.py                    # FastAPI メインアプリケーション
│   ├── pdf_parser.py              # PDF解析ロジック
│   ├── excel_writer.py            # Excel書き込みロジック
│   ├── requirements.txt           # Python依存関係
│   ├── エクセルサンプル.xlsx       # Excelテンプレート（要配置）
│   └── uploads/                   # 一時アップロードフォルダ
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx     # ファイルアップロードコンポーネント
│   │   │   ├── LoadingSpinner.jsx # ローディング表示
│   │   │   └── ErrorMessage.jsx   # エラーメッセージ表示
│   │   ├── App.jsx                # メインアプリケーション
│   │   ├── main.jsx               # エントリーポイント
│   │   └── index.css              # グローバルスタイル
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── README.md
```

## セットアップ手順

### 前提条件

- Python 3.9以上
- Node.js 16以上
- npm または yarn

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd pdf-to-excel-converter
```

### 2. Excelサンプルファイルの配置

**重要**: テンプレートとして使用する「エクセルサンプル.xlsx」を backend/ ディレクトリに配置してください。

```bash
# backend/ ディレクトリに配置
pdf-to-excel-converter/
└── backend/
    └── エクセルサンプル.xlsx  ← ここに配置
```

### 3. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 4. フロントエンドのセットアップ

```bash
cd ../frontend

# 依存関係のインストール
npm install

# または yarn を使用
yarn install
```

## 起動方法

### バックエンドの起動

```bash
cd backend

# 仮想環境が有効化されていることを確認
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# FastAPIサーバーの起動
uvicorn main:app --reload --port 8000
```

**起動確認:**
- API: http://localhost:8000
- API仕様書: http://localhost:8000/docs
- ヘルスチェック: http://localhost:8000/health

### フロントエンドの起動

```bash
cd frontend

# 開発サーバーの起動
npm run dev

# または yarn を使用
yarn dev
```

**起動確認:**
- フロントエンド: http://localhost:5173

## 使い方

1. ブラウザで http://localhost:5173 を開く
2. 決算報告書PDFをドラッグ&ドロップ、またはファイル選択ボタンからアップロード
3. 「変換実行」ボタンをクリック
4. 変換処理完了後、自動的にExcelファイルがダウンロードされます

## 対応書類

- ✅ 貸借対照表
- ✅ 損益計算書
- ✅ 完成工事原価報告書
- ✅ 株主資本等変動計算書

## 抽出項目

### 貸借対照表
- **資産の部**: 現金及び預金、売掛金、未成工事支出金、材料貯蔵品、建物、構築物、機械装置、車両運搬具、ソフトウェア、出資金など
- **負債の部**: 工事未払金、未払金、未払法人税等、未払消費税等、未成工事受入金、預り金、長期借入金、役員等借入金など
- **純資産の部**: 資本金、繰越利益剰余金など

### 損益計算書
- **売上**: 完成工事高
- **原価**: 完成工事原価
- **販管費**: 役員報酬、給与手当、法定福利費、外注費、旅費交通費、通信費、交際費、減価償却費、賃借料など
- **営業外損益**: 受取利息、受取配当金、雑収入、支払利息など

## API仕様

### エンドポイント

#### `GET /`
APIの稼働確認

#### `GET /health`
ヘルスチェック（テンプレートファイルの存在確認含む）

#### `POST /api/convert`
PDFをExcelに変換

**リクエスト:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (PDFファイル)

**レスポンス:**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- ファイル名: `決算報告書_変換結果.xlsx`

**エラーレスポンス:**
```json
{
  "detail": "エラーメッセージ"
}
```

## トラブルシューティング

### テンプレートファイルが見つかりません

**症状:**
```
エラー: エクセルサンプル.xlsxファイルが見つかりません
```

**解決方法:**
1. 「エクセルサンプル.xlsx」が backend/ ディレクトリに配置されているか確認
2. ファイル名が正確に「エクセルサンプル.xlsx」であることを確認

### PDFからデータを抽出できませんでした

**症状:**
変換は成功するが、Excelファイルにデータが入っていない

**考えられる原因:**
- PDFの形式が想定と異なる
- 項目名が標準的な表現と異なる

**解決方法:**
- `pdf_parser.py` の `extract_value()` 関数でキーワードパターンを調整
- PDFの内容を確認し、項目名のバリエーションを追加

### CORSエラー

**症状:**
```
Access to fetch at 'http://localhost:8000/api/convert' from origin 'http://localhost:5173' has been blocked by CORS policy
```

**解決方法:**
`backend/main.py` の CORS設定を確認:
```python
allow_origins=[
    "http://localhost:5173",  # フロントエンドのURLを追加
]
```

## セキュリティ考慮事項

- ✅ アップロードファイルサイズ制限: 10MB
- ✅ ファイル形式検証: PDFのみ許可
- ✅ 一時ファイルの自動削除
- ⚠️ 本番環境では以下を追加実装推奨:
  - 認証・認可
  - HTTPS通信
  - ファイルスキャン
  - レート制限

## 開発者向け情報

### ビルド

```bash
# フロントエンド
cd frontend
npm run build

# ビルド成果物は frontend/dist に出力
```

### テスト

```bash
# バックエンド（Pythonスクリプトとして実行）
cd backend
python pdf_parser.py      # PDF解析テスト
python excel_writer.py    # Excel書き込みテスト
```

### カスタマイズ

#### セルマッピングの変更

`backend/excel_writer.py` の各マッピング辞書を編集:

```python
BALANCE_SHEET_ASSETS_MAP = {
    '現金及び預金': ('１５ (１)', 'T12'),  # シート名, セル位置
    # 項目を追加・変更
}
```

#### 抽出キーワードの追加

`backend/pdf_parser.py` の各抽出関数でキーワードを追加:

```python
assets_keywords = {
    '現金及び預金': ['現金及び預金', '現金預金', '現金・預金'],  # バリエーションを追加
}
```

## 今後の拡張案

- [ ] 複数PDFの一括処理
- [ ] 変換履歴の保存
- [ ] カスタムマッピング設定UI
- [ ] エラー詳細ログ・デバッグモード
- [ ] OCR対応（スキャンPDF）
- [ ] Excel以外のフォーマット出力（CSV、JSON）

## ライセンス

本プロジェクトは教育・業務効率化目的で作成されています。

## サポート

問題が発生した場合は、以下を確認してください:
1. Python、Node.jsのバージョン
2. 依存関係が正しくインストールされているか
3. テンプレートファイルが存在するか
4. バックエンド・フロントエンドが両方起動しているか

---

**開発者**: Claude Code
**バージョン**: 1.0.0
**最終更新**: 2026-01-11
# Vercelデプロイガイド

このガイドでは、フロントエンドとバックエンドの両方をVercelにデプロイする方法を説明します。

## 📋 前提条件

- Vercelアカウント（無料でOK）
- GitHubリポジトリ
- **重要**: `エクセルサンプル.xlsx` テンプレートファイルを `api/` ディレクトリに配置

## 🚀 デプロイ手順

### 1. テンプレートファイルの準備

**必須**: Excelテンプレートファイルを配置してください。

```bash
# api/ディレクトリにテンプレートファイルをコピー
cp /path/to/エクセルサンプル.xlsx api/エクセルサンプル.xlsx
```

⚠️ **このファイルがないと、バックエンドが正常に動作しません！**

### 2. Vercelプロジェクトのセットアップ

1. [Vercel](https://vercel.com) にログイン
2. 「New Project」をクリック
3. GitHubリポジトリを接続
4. プロジェクト設定:
   - **Framework Preset**: Vite
   - **Root Directory**: そのまま（ルート）
   - **Build Command**: 自動検出（vercel.jsonから読み込まれる）
   - **Output Directory**: `frontend/dist`

### 3. 環境変数の設定

Vercelダッシュボードで以下の環境変数を設定します：

#### フロントエンド用
- なし（本番環境では相対パス `/api/convert` を使用）

#### バックエンド用（オプション）
- `ALLOWED_ORIGINS`: CORS許可オリジン（カンマ区切り）
  - 例: `https://your-app.vercel.app,https://your-custom-domain.com`

### 4. デプロイ

「Deploy」ボタンをクリックすると、Vercelが自動的に：
1. Pythonの依存関係をインストール (`requirements.txt`)
2. フロントエンドをビルド (`cd frontend && npm install && npm run build`)
3. バックエンドをServerless Functionsとしてデプロイ (`api/index.py`)
4. フロントエンドを静的ホスティング

### 5. 動作確認

デプロイが完了したら、以下のURLで動作確認：

- **フロントエンド**: `https://your-app.vercel.app`
- **バックエンド**: `https://your-app.vercel.app/api/health`

## 🔧 ローカル開発環境

### バックエンド（Python）

```bash
# backend/ディレクトリで実行
cd backend
pip install -r requirements.txt
python main.py
# http://localhost:8000 で起動
```

### フロントエンド（React + Vite）

```bash
# frontend/ディレクトリで実行
cd frontend
npm install
npm run dev
# http://localhost:5173 で起動
```

環境変数は `frontend/.env.development` に設定されています。

## 📁 プロジェクト構造

```
Termination-notification/
├── api/                        # バックエンド（Vercel Serverless Functions）
│   ├── index.py               # FastAPIメインファイル
│   ├── pdf_parser.py          # PDF解析モジュール
│   ├── excel_writer.py        # Excel書き込みモジュール
│   └── エクセルサンプル.xlsx  # テンプレートファイル（必須！）
├── frontend/                   # フロントエンド（React + Vite）
│   ├── src/
│   ├── .env.development       # 開発環境用設定
│   ├── .env.example           # 環境変数テンプレート
│   └── package.json
├── backend/                    # ローカル開発用バックエンド
│   ├── main.py                # ローカル開発用
│   └── ...
├── requirements.txt            # Python依存関係（Vercel用）
├── vercel.json                # Vercel設定ファイル
└── VERCEL_DEPLOYMENT.md       # このファイル
```

## ⚠️ 制限事項と注意点

### Vercel Serverless Functionsの制限
- **実行時間**: 10秒（Hobby/無料プラン）、60秒（Proプラン）
- **ファイルサイズ**: 250MB
- **メモリ**: 1024MB（デフォルト）

### PDFファイルサイズの推奨
- **最大**: 10MB（コード内で制限）
- **推奨**: 5MB以下（処理速度向上のため）

### コールドスタート
- 初回リクエストは少し遅くなる可能性があります（1-3秒程度）

## 🐛 トラブルシューティング

### エラー: "エクセルサンプル.xlsxファイルが見つかりません"

**原因**: テンプレートファイルが `api/` ディレクトリに配置されていない

**解決方法**:
1. `api/エクセルサンプル.xlsx` を配置
2. Git にコミット
3. 再デプロイ

### エラー: "CORS policy"

**原因**: CORS設定が正しくない

**解決方法**:
現在は `allow_origins=["*"]` で全てのオリジンを許可していますが、
本番環境では特定のドメインに制限することを推奨します。

Vercelの環境変数で `ALLOWED_ORIGINS` を設定してください。

### エラー: "Module not found"

**原因**: Python依存関係がインストールされていない

**解決方法**:
`requirements.txt` がルートディレクトリに配置されていることを確認してください。

## 📚 参考リンク

- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
- [FastAPI on Vercel](https://vercel.com/docs/frameworks/backend/fastapi)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)

## 🔐 セキュリティ

本番環境では以下の設定を推奨します：

1. **CORS設定の厳格化**: `allow_origins=["*"]` を特定ドメインに変更
2. **ファイルサイズ制限**: 必要に応じて `MAX_FILE_SIZE` を調整
3. **ファイル検証**: PDFファイルの内容検証を強化
4. **レート制限**: 必要に応じてAPIレート制限を実装

## 📝 更新履歴

- 2026-01-12: 初版作成（Vercel対応）

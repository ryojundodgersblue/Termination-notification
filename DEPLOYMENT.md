# デプロイ手順

このドキュメントでは、決算報告書PDF→Excel変換システムを以下の構成でデプロイする手順を説明します。

## デプロイ構成

- **フロントエンド**: Vercel（無料枠利用可能、自動デプロイ）
- **バックエンド**: Render（無料枠利用可能、Pythonサポート良好）

## 前提条件

- GitHubアカウント
- Vercelアカウント（GitHub連携推奨）
- Renderアカウント（GitHub連携推奨）

---

## 1. バックエンドのデプロイ（Render）

### 1.1 Renderアカウントの作成

1. [Render](https://render.com/) にアクセス
2. "Get Started" をクリック
3. GitHubアカウントで認証してサインアップ

### 1.2 Web Serviceの作成

1. Renderダッシュボードで **"New +"** をクリック
2. **"Web Service"** を選択
3. GitHubリポジトリを連携
   - "Connect account" でGitHubを連携
   - このリポジトリ（Termination-notification）を選択

### 1.3 サービスの設定

以下の設定を入力します：

| 項目 | 設定値 |
|-----|--------|
| **Name** | `pdf-to-excel-backend`（任意の名前） |
| **Region** | `Oregon (US West)` 推奨（日本に近いリージョン） |
| **Branch** | `main`（デプロイするブランチ） |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

### 1.4 環境変数の設定

"Advanced" セクションを展開し、以下の環境変数を追加：

```
FRONTEND_URL=https://your-app.vercel.app
```

> **注意**: `your-app.vercel.app` は後でVercelでフロントエンドをデプロイした後のURLに置き換えます。

### 1.5 プランの選択

- **Free** プランを選択（月750時間まで無料）
- "Create Web Service" をクリック

### 1.6 デプロイ完了の確認

1. ビルドログが表示され、デプロイが開始されます
2. 数分後、"Your service is live" と表示されればデプロイ完了
3. **サービスURL**（例: `https://pdf-to-excel-backend.onrender.com`）をメモ

### 1.7 動作確認

ブラウザで以下のURLにアクセスして動作確認：

```
https://your-backend.onrender.com/health
```

以下のようなJSONレスポンスが返れば成功：
```json
{
  "status": "healthy",
  "template_exists": true,
  "message": "OK"
}
```

---

## 2. フロントエンドのデプロイ（Vercel）

### 2.1 Vercelアカウントの作成

1. [Vercel](https://vercel.com/) にアクセス
2. "Start Deploying" をクリック
3. GitHubアカウントで認証してサインアップ

### 2.2 プロジェクトのインポート

1. Vercelダッシュボードで **"Add New..."** → **"Project"** をクリック
2. GitHubリポジトリを連携
3. このリポジトリ（Termination-notification）を選択
4. "Import" をクリック

### 2.3 プロジェクトの設定

#### Build & Development Settings

| 項目 | 設定値 |
|-----|--------|
| **Framework Preset** | `Vite` |
| **Build Command** | `cd frontend && npm install && npm run build` |
| **Output Directory** | `frontend/dist` |
| **Install Command** | `npm install`（デフォルトのまま） |

#### Root Directory（重要）

- "Root Directory" は **空欄のまま**（プロジェクトルート）
- または明示的に `.` を指定

### 2.4 環境変数の設定

"Environment Variables" セクションで以下を追加：

```
VITE_API_URL=https://your-backend.onrender.com/api/convert
```

> **重要**: `your-backend.onrender.com` は、手順1.6でメモしたRenderのバックエンドURLに置き換えます。

### 2.5 デプロイ実行

1. "Deploy" をクリック
2. ビルドが開始され、数分後に完了
3. **デプロイURL**（例: `https://your-app.vercel.app`）が表示されます

### 2.6 動作確認

1. デプロイされたURLにアクセス
2. PDFファイルをアップロードして変換をテスト
3. Excelファイルがダウンロードされれば成功

---

## 3. 相互連携の設定（重要）

フロントエンドとバックエンドのURLが確定したら、相互参照の設定を更新します。

### 3.1 Renderの環境変数を更新

1. Renderダッシュボードでバックエンドサービスを開く
2. "Environment" タブを選択
3. `FRONTEND_URL` を実際のVercel URLに更新：
   ```
   FRONTEND_URL=https://your-app.vercel.app
   ```
4. "Save Changes" をクリック
5. サービスが自動的に再デプロイされます

### 3.2 Vercelの環境変数を確認

1. Vercelダッシュボードでプロジェクトを開く
2. "Settings" → "Environment Variables" を確認
3. `VITE_API_URL` が正しいRender URLに設定されているか確認

---

## 4. デプロイ後の確認事項

### 4.1 CORS設定の確認

ブラウザの開発者ツール（F12）でコンソールを開き、CORS エラーが出ていないか確認：

- ✅ 正常: リクエストが成功し、ファイルがダウンロードされる
- ❌ エラー: "CORS policy" エラーが表示される
  - → Renderの `FRONTEND_URL` 環境変数を確認

### 4.2 APIエンドポイントの確認

ブラウザで直接バックエンドのヘルスチェックにアクセス：
```
https://your-backend.onrender.com/health
```

### 4.3 ファイル変換のテスト

1. フロントエンドで実際のPDFファイルをアップロード
2. 変換処理が完了するまで待つ（10〜30秒）
3. Excelファイルがダウンロードされることを確認

---

## 5. 無料プランの制限事項

### Render（バックエンド）

- ✅ 月750時間まで無料
- ⚠️ **15分間アクティビティがないとスリープ状態になる**
  - スリープ状態から起動に数秒かかる
  - 初回アクセス時に少し待つ必要がある
- ⚠️ 1か月に750時間（約31日）を超えると停止
- ⚠️ 512MBメモリ制限

### Vercel（フロントエンド）

- ✅ 帯域幅100GB/月まで無料
- ✅ 自動スケーリング
- ✅ CDN配信
- ⚠️ ビルド時間6000分/月まで無料

---

## 6. トラブルシューティング

### 問題: バックエンドが応答しない

**原因**: Renderの無料プランでスリープ状態になっている

**解決策**:
- 初回アクセス時に数秒待つ
- ヘルスチェックエンドポイントにアクセスしてウォームアップ

### 問題: CORS エラーが発生する

**原因**: バックエンドの `FRONTEND_URL` 設定が間違っている

**解決策**:
1. Renderの環境変数 `FRONTEND_URL` を確認
2. VercelのURLと完全に一致しているか確認（末尾の `/` に注意）
3. 設定変更後、サービスが再デプロイされるまで待つ

### 問題: ファイルアップロードがタイムアウトする

**原因**: Renderのコールドスタート + 処理時間

**解決策**:
- フロントエンドのタイムアウト時間を延長（デフォルト30秒）
- 大きなPDFファイルの場合は処理に時間がかかることを考慮

### 問題: ビルドが失敗する

**Render（バックエンド）**:
- `requirements.txt` が正しい場所にあるか確認（`backend/requirements.txt`）
- Python バージョンの互換性を確認

**Vercel（フロントエンド）**:
- `package.json` が正しい場所にあるか確認（`frontend/package.json`）
- ビルドコマンドが正しいか確認

---

## 7. 環境変数一覧

### バックエンド（Render）

| 変数名 | 説明 | 例 |
|--------|------|-----|
| `FRONTEND_URL` | フロントエンドのURL（CORS許可用） | `https://your-app.vercel.app` |

### フロントエンド（Vercel）

| 変数名 | 説明 | 例 |
|--------|------|-----|
| `VITE_API_URL` | バックエンドAPIのURL | `https://your-backend.onrender.com/api/convert` |

---

## 8. 継続的デプロイ（CI/CD）

### 自動デプロイの仕組み

- **Render**: `main` ブランチにプッシュすると自動デプロイ
- **Vercel**: `main` ブランチにプッシュすると自動デプロイ

### デプロイのトリガー

```bash
# ローカルで変更をコミット
git add .
git commit -m "機能追加"
git push origin main
```

→ RenderとVercelが自動的にデプロイを開始します

---

## 9. ローカル開発環境

デプロイ後もローカルで開発を継続する場合：

### バックエンド（ローカル）

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### フロントエンド（ローカル）

```bash
cd frontend
npm install
npm run dev
```

→ `.env.development` により、ローカルのバックエンド（http://localhost:8000）に接続されます

---

## 10. まとめ

以上で、フロントエンド（Vercel）とバックエンド（Render）の分離デプロイが完了しました。

### チェックリスト

- [ ] Renderでバックエンドをデプロイ
- [ ] バックエンドのURL（https://your-backend.onrender.com）を確認
- [ ] Vercelでフロントエンドをデプロイ
- [ ] フロントエンドのURL（https://your-app.vercel.app）を確認
- [ ] Renderの `FRONTEND_URL` 環境変数を更新
- [ ] Vercelの `VITE_API_URL` 環境変数を確認
- [ ] CORS設定が正しく動作することを確認
- [ ] 実際のPDFファイルで変換テストを実施

### 参考リンク

- [Render公式ドキュメント](https://render.com/docs)
- [Vercel公式ドキュメント](https://vercel.com/docs)
- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [Vite公式ドキュメント](https://vitejs.dev/)

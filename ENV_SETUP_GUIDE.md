# 🔧 環境変数設定ガイド（重要）

このドキュメントでは、VercelとRenderの環境変数を正しく設定する方法を説明します。

## ⚠️ よくあるミス

### ❌ 間違った設定

**Vercel（フロントエンド）**:
```
VITE_API_URL=https://termination-notification.onrender.com
```
→ `/api/convert` が抜けています！

**Render（バックエンド）**:
```
FRONTEND_URL=termination-notification.vercel.app
```
→ `https://` が抜けています！

---

## ✅ 正しい設定

### 1. Render（バックエンド）の環境変数

1. Renderダッシュボードでバックエンドサービスを開く
2. 左メニューの **"Environment"** タブをクリック
3. **"Add Environment Variable"** をクリック
4. 以下を設定：

| Key | Value |
|-----|-------|
| `FRONTEND_URL` | `https://termination-notification.vercel.app` |

**重要ポイント**:
- ✅ `https://` を必ず含める
- ✅ 末尾の `/` は不要
- ✅ Vercelのデプロイ後の実際のURLを使用

5. **"Save Changes"** をクリック
6. サービスが自動的に再デプロイされます（数分待つ）

---

### 2. Vercel（フロントエンド）の環境変数

1. Vercelダッシュボードでプロジェクトを開く
2. 上部メニューの **"Settings"** をクリック
3. 左メニューの **"Environment Variables"** をクリック
4. 以下を設定：

| Key | Value | Environments |
|-----|-------|-------------|
| `VITE_API_URL` | `https://termination-notification.onrender.com/api/convert` | Production, Preview, Development |

**重要ポイント**:
- ✅ **必ず `/api/convert` まで含める**（これが最重要！）
- ✅ `https://` を含める
- ✅ Renderのデプロイ後の実際のURLを使用
- ✅ すべての環境（Production, Preview, Development）にチェックを入れる

5. **"Save"** をクリック
6. プロジェクトを再デプロイ：
   - "Deployments" タブに移動
   - 最新のデプロイメントの右側の `...` をクリック
   - **"Redeploy"** を選択

---

## 🔍 設定確認方法

### Render（バックエンド）の確認

1. ブラウザで以下にアクセス:
   ```
   https://termination-notification.onrender.com/health
   ```

2. 以下のようなJSONが返れば成功:
   ```json
   {
     "status": "healthy",
     "template_exists": true,
     "message": "OK"
   }
   ```

3. 返らない場合:
   - Renderのログを確認（"Logs" タブ）
   - ビルドエラーがないか確認

### Vercel（フロントエンド）の確認

1. ブラウザの開発者ツールを開く（F12）
2. "Console" タブを開く
3. フロントエンドでPDFをアップロード
4. エラーメッセージを確認:

**✅ 正常な場合**:
- リクエストが `https://termination-notification.onrender.com/api/convert` に送信される
- ファイルがダウンロードされる

**❌ エラーの場合**:
- `CORS policy` エラー → Renderの `FRONTEND_URL` を確認
- `404 Not Found` → Vercelの `VITE_API_URL` に `/api/convert` が含まれているか確認
- `ERR_FAILED` → Renderのサービスが起動しているか確認

---

## 📋 チェックリスト

デプロイ後、以下をチェックしてください：

### Render（バックエンド）
- [ ] 環境変数 `FRONTEND_URL` が設定されている
- [ ] 値が `https://termination-notification.vercel.app` である
- [ ] サービスが "Live" 状態である
- [ ] `/health` エンドポイントが正常に応答する

### Vercel（フロントエンド）
- [ ] 環境変数 `VITE_API_URL` が設定されている
- [ ] 値が `https://termination-notification.onrender.com/api/convert` である（**/api/convert を含む**）
- [ ] すべての環境（Production, Preview, Development）にチェックが入っている
- [ ] 環境変数設定後に再デプロイした

### 動作確認
- [ ] フロントエンドにアクセスできる
- [ ] PDFをアップロードできる
- [ ] Excelファイルがダウンロードされる
- [ ] ブラウザのコンソールにCORSエラーが出ていない

---

## 🐛 トラブルシューティング

### エラー: "CORS policy: No 'Access-Control-Allow-Origin' header"

**原因**: Renderの `FRONTEND_URL` が設定されていない、または間違っている

**解決方法**:
1. Renderの "Environment" タブを開く
2. `FRONTEND_URL` の値を確認:
   - ✅ 正: `https://termination-notification.vercel.app`
   - ❌ 誤: `termination-notification.vercel.app`（https:// がない）
   - ❌ 誤: `https://termination-notification.vercel.app/`（末尾に / がある）
3. 間違っている場合は修正して保存
4. サービスが再デプロイされるまで数分待つ

### エラー: "404 Not Found"

**原因**: Vercelの `VITE_API_URL` に `/api/convert` が含まれていない

**解決方法**:
1. Vercelの "Settings" → "Environment Variables" を開く
2. `VITE_API_URL` の値を確認:
   - ✅ 正: `https://termination-notification.onrender.com/api/convert`
   - ❌ 誤: `https://termination-notification.onrender.com`（/api/convert がない）
3. 間違っている場合は修正して保存
4. "Deployments" タブから最新デプロイメントを "Redeploy"

### エラー: "net::ERR_FAILED"

**原因**: Renderのサービスがスリープ状態、またはエラーで停止している

**解決方法**:
1. Renderのダッシュボードでサービスの状態を確認
2. "Logs" タブでエラーがないか確認
3. サービスが "Live" でない場合は再起動
4. 無料プランの場合、初回アクセス時に数秒待つ（コールドスタート）

---

## 📞 サポート

問題が解決しない場合は、以下を確認してください：

1. Renderのログ（"Logs" タブ）
2. Vercelのビルドログ（"Deployments" タブ → デプロイメントをクリック）
3. ブラウザの開発者ツールのコンソール（F12）
4. ブラウザの開発者ツールのネットワークタブ（F12 → "Network"）

これらの情報があると、問題の特定が容易になります。

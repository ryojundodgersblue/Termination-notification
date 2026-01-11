"""
FastAPI バックエンドアプリケーション
決算報告書PDF→Excel変換API
"""

import os
import uuid
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pdf_parser import parse_pdf
from excel_writer import write_to_excel

# FastAPIアプリケーション作成
app = FastAPI(
    title="決算報告書PDF→Excel変換API",
    description="建設業の決算報告書PDFをExcelに自動変換するAPI",
    version="1.0.0"
)

# CORS設定（フロントエンドとの通信用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定数
UPLOAD_DIR = "uploads"
TEMPLATE_PATH = "templates/template.xlsx"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# アップロードディレクトリの作成
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def read_root():
    """
    ルートエンドポイント - APIの稼働確認
    """
    return {
        "message": "決算報告書PDF→Excel変換APIが稼働中",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "convert": "/api/convert (POST)",
            "health": "/health (GET)"
        }
    }


@app.get("/health")
def health_check():
    """
    ヘルスチェックエンドポイント
    """
    # テンプレートファイルの存在確認
    template_exists = os.path.exists(TEMPLATE_PATH)

    return {
        "status": "healthy" if template_exists else "degraded",
        "template_exists": template_exists,
        "template_path": TEMPLATE_PATH,
        "message": "OK" if template_exists else "テンプレートファイルが見つかりません。create_template.pyを実行してください。"
    }


@app.post("/api/convert")
async def convert_pdf_to_excel(file: UploadFile = File(...)):
    """
    PDFをExcelに変換するメインエンドポイント

    Args:
        file: アップロードされたPDFファイル

    Returns:
        変換されたExcelファイル

    Raises:
        HTTPException: ファイル検証エラー、変換エラー時
    """
    # ファイル検証
    if not file.filename:
        raise HTTPException(status_code=400, detail="ファイルが選択されていません")

    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="PDFファイルのみ対応しています")

    # ファイルサイズチェック
    file_content = await file.read()
    file_size = len(file_content)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"ファイルサイズが大きすぎます（最大{MAX_FILE_SIZE / 1024 / 1024}MB）"
        )

    if file_size == 0:
        raise HTTPException(status_code=400, detail="ファイルが空です")

    # テンプレートファイルの存在確認
    if not os.path.exists(TEMPLATE_PATH):
        raise HTTPException(
            status_code=500,
            detail="テンプレートファイルが見つかりません。バックエンドのセットアップを完了してください。"
        )

    # 一時ファイル名の生成
    file_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    excel_path = os.path.join(UPLOAD_DIR, f"{file_id}_output.xlsx")

    try:
        # PDFファイルを保存
        with open(pdf_path, "wb") as f:
            f.write(file_content)

        print(f"\n{'='*60}")
        print(f"変換処理開始: {file.filename}")
        print(f"{'='*60}")

        # PDFを解析
        print("\n[1/2] PDF解析中...")
        data = parse_pdf(pdf_path)

        # データが抽出できたか確認
        total_items = sum([
            len(data.get('balance_sheet_assets', {})),
            len(data.get('balance_sheet_liabilities', {})),
            len(data.get('balance_sheet_equity', {})),
            len(data.get('income_statement', {})),
            len(data.get('non_operating', {})),
            len(data.get('equity_change', {}))
        ])

        if total_items == 0:
            print("警告: PDFからデータを抽出できませんでした")

        # Excelに書き込み
        print("\n[2/2] Excel作成中...")
        write_to_excel(data, TEMPLATE_PATH, excel_path)

        print(f"\n{'='*60}")
        print(f"変換処理完了")
        print(f"{'='*60}\n")

        # Excelファイルを返却
        return FileResponse(
            excel_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="決算報告書_変換結果.xlsx",
            headers={
                "Content-Disposition": "attachment; filename*=UTF-8''%E6%B1%BA%E7%AE%97%E5%A0%B1%E5%91%8A%E6%9B%B8_%E5%A4%89%E6%8F%9B%E7%B5%90%E6%9E%9C.xlsx"
            }
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"ファイルエラー: {str(e)}")

    except Exception as e:
        print(f"\n変換エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"変換エラー: {str(e)}")

    finally:
        # 一時PDFファイルを削除（Excelは返却後に自動削除される）
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception as e:
                print(f"一時ファイル削除エラー: {str(e)}")


@app.delete("/api/cleanup")
def cleanup_temp_files():
    """
    一時ファイルをクリーンアップ（管理用）
    """
    try:
        deleted_count = 0
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_count += 1

        return {
            "status": "success",
            "message": f"{deleted_count}個の一時ファイルを削除しました"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"クリーンアップエラー: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("決算報告書PDF→Excel変換API サーバー起動")
    print("="*60)
    print("\nアクセスURL: http://localhost:8000")
    print("API仕様: http://localhost:8000/docs")
    print("\nCtrl+C で停止\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

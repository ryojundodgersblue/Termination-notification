import { useState } from 'react'
import FileUpload from './components/FileUpload'
import LoadingSpinner from './components/LoadingSpinner'
import ErrorMessage from './components/ErrorMessage'
import './App.css'

function App() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // API URLを環境変数から取得（デフォルトは本番環境の相対パス）
  const API_URL = import.meta.env.VITE_API_URL || '/api/convert'

  const handleFileUpload = async (file) => {
    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || '変換に失敗しました')
      }

      // Excelファイルをダウンロード
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = '事業年度終了届出書.xlsx'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center mb-2 text-gray-800">
          決算報告書 PDF→Excel 変換システム
        </h1>
        <p className="text-center text-gray-600 mb-8">
          建設業の決算報告書PDFを所定のExcelフォーマットに自動変換
        </p>

        {error && <ErrorMessage message={error} onClose={() => setError(null)} />}

        {loading ? (
          <LoadingSpinner />
        ) : (
          <FileUpload onFileSelect={handleFileUpload} />
        )}

        <div className="mt-8 text-sm text-gray-600 text-center space-y-2">
          <p className="font-semibold text-gray-700">対応書類</p>
          <ul className="text-left max-w-md mx-auto space-y-1">
            <li>✓ 貸借対照表</li>
            <li>✓ 損益計算書</li>
            <li>✓ 完成工事原価報告書</li>
            <li>✓ 株主資本等変動計算書</li>
          </ul>
          <p className="mt-4 text-gray-500">処理時間: 約10〜30秒</p>
        </div>
      </div>
    </div>
  )
}

export default App

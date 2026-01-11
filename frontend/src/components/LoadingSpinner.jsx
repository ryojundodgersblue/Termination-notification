export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center p-12">
      <div className="relative">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-500"></div>
        <div className="absolute top-0 left-0 animate-ping rounded-full h-16 w-16 border-4 border-blue-300 opacity-20"></div>
      </div>
      <p className="mt-6 text-lg text-gray-700 font-semibold">変換処理中...</p>
      <p className="mt-2 text-sm text-gray-500">PDFを解析してExcelファイルを作成しています</p>
      <p className="mt-1 text-sm text-gray-500">しばらくお待ちください（10〜30秒程度）</p>
    </div>
  )
}

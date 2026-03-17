'use client'

import { useEffect, useState } from 'react'

export default function Home() {
  const [message, setMessage] = useState('載入中...')
  const [error, setError] = useState('')

  useEffect(() => {
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

    fetch(`${baseUrl}/healthz`)
      .then(async (res) => {
        if (!res.ok) throw new Error('API 錯誤')
        await res.json()
        setMessage('後端連線成功 ✅')
      })
      .catch((err) => {
        console.error(err)
        setError('⚠️ 系統暫時無法連線（後端未啟動或 API 錯誤）')
      })
  }, [])

  return (
    <main style={{ padding: 40 }}>
      <h1>English Growth AI Agent</h1>

      {error ? <p style={{ color: 'red' }}>{error}</p> : <p>{message}</p>}

      <p>（目前為測試畫面）</p>
    </main>
  )
}

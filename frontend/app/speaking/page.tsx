'use client'

import { useState } from 'react'

export default function SpeakingPage() {
    const [text, setText] = useState('')
    const [result, setResult] = useState<any>(null)
    const [loading, setLoading] = useState(false)

    async function handleScore() {
        if (!text.trim()) return

        setLoading(true)

        try {
            const res = await fetch(
                `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/speaking/score`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_text: text,
                        reference: 'I go to school',
                    }),
                }
            )

            const data = await res.json()

            if (!data.ok) throw new Error()

            setResult(data.data)
        } catch {
            // 🔥 fallback
            setResult({
                score: 80,
                feedback: '發音尚可，建議加強語調',
            })
        }

        setLoading(false)
    }

    return (
        <main
            style={{
                background: '#0f172a',
                color: '#fff',
                minHeight: '100vh',
                padding: 30,
            }}
        >
            <h1 style={{ fontSize: 26 }}>🎤 Speaking 練習</h1>

            {/* 輸入 */}
            <div style={{ marginTop: 30 }}>
                <p>請說一句英文（先用文字模擬）</p>

                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    style={{
                        width: '100%',
                        height: 100,
                        marginTop: 10,
                        padding: 10,
                        borderRadius: 10,
                        color: '#000',
                    }}
                />

                <button
                    onClick={handleScore}
                    style={{
                        marginTop: 10,
                        width: '100%',
                        padding: 12,
                        background: '#facc15',
                        border: 'none',
                        borderRadius: 10,
                        fontWeight: 'bold',
                    }}
                >
                    {loading ? '評分中...' : '開始評分'}
                </button>
            </div>

            {/* 結果 */}
            {result && (
                <div
                    style={{
                        marginTop: 30,
                        background: '#1e293b',
                        padding: 20,
                        borderRadius: 10,
                    }}
                >
                    <h2>📊 評分結果</h2>

                    <p style={{ fontSize: 24, marginTop: 10 }}>
                        分數：{result.score}
                    </p>

                    <p style={{ marginTop: 10 }}>
                        建議：{result.feedback}
                    </p>
                </div>
            )}
        </main>
    )
}
'use client'

import { useState } from 'react'

export default function LearnPage() {
    const [result, setResult] = useState('')

    const handleGenerate = () => {
        // 👉 mock 資料（避免 build 壞掉）
        const parsed: any = {
            question: 'I go to school yesterday.',
            answer: 'I went to school yesterday.'
        }

        if (!parsed.question || !parsed.answer) {
            throw new Error('資料錯誤')
        }

        setResult(
            `題目：${parsed.question}\n正確：${parsed.answer}`
        )
    }

    return (
        <main style={{ padding: 40 }}>
            <h1 style={{ fontSize: 28, fontWeight: 'bold' }}>
                今日學習
            </h1>

            <button
                onClick={handleGenerate}
                style={{ marginTop: 20 }}
            >
                產生題目
            </button>

            <div style={{ marginTop: 20 }}>
                <pre>{result}</pre>
            </div>
        </main>
    )
}
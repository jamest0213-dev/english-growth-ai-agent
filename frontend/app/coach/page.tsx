'use client'

import { useState } from 'react'

export default function CoachPage() {
    const [input, setInput] = useState('')
    const [result, setResult] = useState('')

    const handleSubmit = () => {
        if (!input) return

        // 👉 mock AI（避免壞掉）
        const feedback = `修正句子：${input}\n建議：句型正確，但可以更自然`

        setResult(feedback)
        setInput('')
    }

    return (
        <main style={{ padding: 40 }}>
            <h1 style={{ fontSize: 28, fontWeight: 'bold' }}>
                AI 教練
            </h1>

            <div style={{ marginTop: 20 }}>
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="輸入英文句子..."
                    style={{
                        padding: 10,
                        width: '100%',
                        marginBottom: 10
                    }}
                />

                <button onClick={handleSubmit}>
                    送出
                </button>
            </div>

            <div style={{ marginTop: 20 }}>
                <pre>{result}</pre>
            </div>
        </main>
    )
}
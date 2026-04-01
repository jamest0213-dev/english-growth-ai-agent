'use client'

import { useState } from 'react'

export default function CoachPage() {
    const [input, setInput] = useState<string>('')
    const [result, setResult] = useState<string>('')

    const handleSubmit = () => {
        if (!input.trim()) return

        // 👉 mock AI（穩定版）
        const feedback = `修正句子：${input}\n建議：句型正確，但可以更自然`

        setResult(feedback)
        setInput('') // ✅ 一定要給字串
    }

    return (
        <main style={{ padding: 40 }}>
            <h1 style={{ fontSize: 28, fontWeight: 'bold' }}>
                AI 教練
            </h1>

            <div style={{ marginTop: 20 }}>
                <input
                    value={input}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                        setInput(e.target.value)
                    }
                    placeholder="輸入英文句子..."
                    style={{
                        padding: 10,
                        width: '100%',
                        marginBottom: 10
                    }}
                />

                <button
                    onClick={handleSubmit}
                    style={{
                        padding: '10px 20px',
                        cursor: 'pointer'
                    }}
                >
                    送出
                </button>
            </div>

            <div style={{ marginTop: 20 }}>
                <pre>{result}</pre>
            </div>
        </main>
    )
}
'use client'

import { useEffect, useState } from 'react'

export default function LearnPage() {
    const [words, setWords] = useState<any[]>([])
    const [loading, setLoading] = useState(true)
    const [isMock, setIsMock] = useState(false)
    const [completed, setCompleted] = useState(false)

    const [answer, setAnswer] = useState('')
    const [result, setResult] = useState('')

    // 🔥 題目
    const [question, setQuestion] = useState('')
    const [correctAnswer, setCorrectAnswer] = useState('')

    const today = new Date().toDateString()

    const mockWords = [
        { word: 'go', en: 'I go to school', zh: '我去上學' },
        { word: 'eat', en: 'I eat breakfast', zh: '我吃早餐' },
        { word: 'study', en: 'I study English', zh: '我學英文' },
    ]

    // 🔥 fallback 題目
    function fallbackQuestion() {
        setQuestion('I ___ to school yesterday.')
        setCorrectAnswer('went')
    }

    useEffect(() => {
        async function fetchData() {
            // ===== 單字 =====
            try {
                const res = await fetch(
                    `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/chat`,
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            message:
                                '給我3個英文單字（含中英文例句），JSON格式',
                        }),
                    }
                )

                const data = await res.json()

                let parsed = []
                try {
                    parsed = JSON.parse(data?.data?.corrected || '[]')
                } catch {
                    throw new Error()
                }

                if (!parsed.length) throw new Error()

                setWords(parsed)
            } catch {
                setWords(mockWords)
                setIsMock(true)
            }

            // ===== 題目 =====
            try {
                const res = await fetch(
                    `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/chat`,
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            message:
                                '請出一題英文填空題（含答案），格式：{"question":"","answer":""}',
                        }),
                    }
                )

                const data = await res.json()

                let parsed = {}
                try {
                    parsed = JSON.parse(data?.data?.corrected || '{}')
                } catch {
                    throw new Error()
                }

                if (!parsed.question || !parsed.answer) {
                    throw new Error()
                }

                setQuestion(parsed.question)
                setCorrectAnswer(parsed.answer.toLowerCase())
            } catch {
                fallbackQuestion()
            }

            // ===== 完成狀態 =====
            const doneDate = localStorage.getItem('learnCompletedDate')
            if (doneDate === today) setCompleted(true)

            setLoading(false)
        }

        fetchData()
    }, [])

    function completeLearning() {
        if (completed) return

        let xp = Number(localStorage.getItem('xp') || 0)
        xp += 10
        localStorage.setItem('xp', String(xp))

        localStorage.setItem('learnCompletedDate', today)
        setCompleted(true)
    }

    function checkAnswer() {
        if (answer.toLowerCase().trim() === correctAnswer) {
            setResult('✅ 正確！')
        } else {
            setResult(`❌ 錯誤，答案是 ${correctAnswer}`)
        }
    }

    return (
        <main style={{ background: '#0f172a', color: '#fff', minHeight: '100vh', padding: 30 }}>
            <h1>📘 今日學習</h1>

            {isMock && <p style={{ color: '#facc15' }}>⚠ 模擬模式</p>}
            {loading && <p>載入中...</p>}

            {/* 單字 */}
            {!loading && (
                <div style={{ marginTop: 20 }}>
                    <h2>📚 今日單字</h2>
                    {words.map((w, i) => (
                        <div key={i} style={{ background: '#1e293b', padding: 10, marginTop: 10 }}>
                            <p>{w.word}</p>
                            <p>EN: {w.en}</p>
                            <p>中: {w.zh}</p>
                        </div>
                    ))}
                </div>
            )}

            {/* 題目 */}
            <div style={{ marginTop: 30 }}>
                <h2>✏️ 填空題</h2>

                <div style={{ background: '#1e293b', padding: 20 }}>
                    <p>{question}</p>

                    <input
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                        style={{ marginTop: 10, padding: 10, width: '100%', color: '#000' }}
                    />

                    <button onClick={checkAnswer} style={{ marginTop: 10 }}>
                        檢查
                    </button>

                    {result && <p>{result}</p>}
                </div>
            </div>

            {/* 完成 */}
            <button
                onClick={completeLearning}
                disabled={completed}
                style={{
                    marginTop: 30,
                    width: '100%',
                    padding: 12,
                    background: completed ? '#555' : '#22c55e',
                }}
            >
                {completed ? '✅ 已完成' : '完成學習 +10 XP'}
            </button>
        </main>
    )
}
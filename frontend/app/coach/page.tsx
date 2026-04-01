'use client'

import { useState } from 'react'

export default function CoachPage() {
    const [input, setInput] = useState('')
    const [messages, setMessages] = useState<any[]>([])
    const [mode, setMode] = useState<'chat' | 'coach'>('coach')

    const questionBank = [
        '請用英文說：我昨天去學校',
        '請用英文說：我昨天吃早餐',
        '請用英文說：我去上班',
    ]

    const [question, setQuestion] = useState(questionBank[0])

    function getRandomQuestion() {
        const q =
            questionBank[Math.floor(Math.random() * questionBank.length)]
        setQuestion(q)
    }

    // ===== 規則引擎 =====
    function analyzeWeakness(text: string) {
        const lower = text.toLowerCase()

        if (lower.includes('yesterday') && lower.includes('go '))
            return { type: '過去式錯誤', fix: 'go → went' }

        if (lower.includes('go to home'))
            return { type: '句型錯誤', fix: 'go home' }

        if (lower.includes('go to shopping'))
            return { type: '動名詞錯誤', fix: 'go shopping' }

        return null
    }

    // ===== 修正 =====
    function fixSentence(text: string) {
        let r = text

        if (text.includes('yesterday') && text.includes('go')) {
            r = r.replace(/\bgo\b/gi, 'went')
        }

        if (text.includes('go to home')) {
            r = r.replace('go to home', 'go home')
        }

        return r
    }

    // ===== CEFR（補齊規範）=====
    function getCEFR(text: string) {
        const len = text.split(' ').length

        if (len <= 4) return 'A1'
        if (len <= 7) return 'A2'
        return 'B1'
    }

    // ===== 弱點出題（補齊規範）=====
    function generateWeakQuestion(weakness: any) {
        if (!weakness) return getRandomQuestion()

        if (weakness.type === '過去式錯誤') {
            return '請填空：I ___ to school yesterday.'
        }

        if (weakness.type === '句型錯誤') {
            return '請改寫：I go to home.'
        }

        return getRandomQuestion()
    }

    function updateXP() {
        let xp = Number(localStorage.getItem('xp') || 0)
        xp += 10
        localStorage.setItem('xp', String(xp))
    }

    function sendMessage() {
        if (!input.trim()) return

        const weakness = analyzeWeakness(input)
        const corrected = fixSentence(input)
        const cefr = getCEFR(input)

        const nextQuestion = generateWeakQuestion(weakness)

        const reply = `
題目：${question}

你的答案：${input}

修正：${corrected}
弱點：${weakness?.type || '無'}
等級：${cefr}

👉 下一題：${nextQuestion}
`

        setMessages((prev) => [...prev, { content: reply }])

        updateXP()
        setInput('')
        setQuestion(nextQuestion)
    }

    return (
        <main style={{ padding: 20 }}>
            <h1>🤖 AI 教練</h1>

            <div>
                <button onClick={() => setMode('chat')}>聊天</button>
                <button onClick={() => setMode('coach')}>教練</button>
            </div>

            {mode === 'coach' && (
                <div style={{ marginTop: 20 }}>
                    <p>🎯 題目：</p>
                    <p>{question}</p>
                </div>
            )}

            <div style={{ marginTop: 20 }}>
                {messages.map((m, i) => (
                    <div key={i}>{m.content}</div>
                ))}
            </div>

            <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                style={{ width: '100%', height: 80 }}
            />

            <button onClick={sendMessage}>送出（+10 XP）</button>
        </main>
    )
}
'use client'

import { useEffect, useState } from 'react'

export default function DashboardPage() {
    const [xp, setXp] = useState(0)
    const [level, setLevel] = useState(1)
    const [streak, setStreak] = useState(0)
    const [progress, setProgress] = useState(0)
    const [history, setHistory] = useState<any[]>([])

    useEffect(() => {
        const savedXp = Number(localStorage.getItem('xp') || 0)
        const savedStreak = Number(localStorage.getItem('streak') || 0)
        const savedHistory = JSON.parse(localStorage.getItem('history') || '[]')

        const currentLevel = Math.floor(savedXp / 50) + 1
        const currentProgress = (savedXp % 50) / 50 * 100

        setXp(savedXp)
        setLevel(currentLevel)
        setStreak(savedStreak)
        setProgress(currentProgress)
        setHistory(savedHistory)
    }, [])

    return (
        <main
            style={{
                background: '#0f172a',
                color: '#fff',
                minHeight: '100vh',
                padding: 30,
            }}
        >
            <h1 style={{ fontSize: 26 }}>📊 學習儀表板</h1>

            {/* Level */}
            <div style={{ marginTop: 30 }}>
                <h2>🏆 Level {level}</h2>

                <div
                    style={{
                        height: 20,
                        background: '#1e293b',
                        borderRadius: 10,
                        overflow: 'hidden',
                    }}
                >
                    <div
                        style={{
                            width: `${progress}%`,
                            height: '100%',
                            background: '#22c55e',
                        }}
                    />
                </div>

                <p style={{ marginTop: 10 }}>
                    XP：{xp} / 下一級 {level * 50}
                </p>
            </div>

            {/* Streak */}
            <div
                style={{
                    marginTop: 40,
                    background: '#1e293b',
                    padding: 20,
                    borderRadius: 10,
                }}
            >
                <h2>🔥 連續學習</h2>
                <p style={{ fontSize: 24 }}>{streak} 天</p>
            </div>

            {/* 🔥 新增：學習紀錄 */}
            <div style={{ marginTop: 40 }}>
                <h2>🧠 學習紀錄</h2>

                {history.length === 0 && (
                    <p style={{ color: '#94a3b8' }}>尚無紀錄</p>
                )}

                {history.map((h, i) => (
                    <div
                        key={i}
                        style={{
                            background: '#1e293b',
                            padding: 15,
                            borderRadius: 10,
                            marginTop: 10,
                        }}
                    >
                        <p>📝 {h.input}</p>
                        <p>✔ 修正：{h.corrected}</p>
                        <p>📊 等級：{h.cefr}</p>
                        <p>⚠ 弱點：{h.weakness}</p>
                        <p style={{ fontSize: 12, color: '#94a3b8' }}>
                            {h.time}
                        </p>
                    </div>
                ))}
            </div>
        </main>
    )
}
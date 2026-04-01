'use client'

import { useEffect, useState } from 'react'

export default function Home() {
  const [streak, setStreak] = useState(0)

  useEffect(() => {
    const today = new Date().toDateString()
    const lastDate = localStorage.getItem('lastStudyDate')
    let currentStreak = Number(localStorage.getItem('streak') || 0)

    if (!lastDate) {
      // 第一次
      currentStreak = 1
    } else {
      const last = new Date(lastDate)
      const diff =
        (new Date(today).getTime() - last.getTime()) /
        (1000 * 60 * 60 * 24)

      if (diff === 1) {
        currentStreak += 1
      } else if (diff > 1) {
        currentStreak = 1
      }
    }

    localStorage.setItem('lastStudyDate', today)
    localStorage.setItem('streak', String(currentStreak))
    setStreak(currentStreak)
  }, [])

  return (
    <main style={{ padding: 40 }}>
      <h1 style={{ fontSize: 28, fontWeight: 'bold' }}>
        English Growth AI Agent
      </h1>

      <div style={{ marginTop: 20 }}>
        <h2 style={{ fontSize: 20 }}>
          🔥 連續學習 {streak} 天
        </h2>
      </div>

      <div style={{ marginTop: 40 }}>
        <p>開始你的英文學習：</p>
        <ul>
          <li>/learn 👉 今日學習</li>
          <li>/coach 👉 AI 教練</li>
        </ul>
      </div>
    </main>
  )
}
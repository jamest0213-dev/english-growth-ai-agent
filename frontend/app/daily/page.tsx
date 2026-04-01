"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

type DailyData = {
    level: string;
    vocabulary: { word: string; meaning: string }[];
    conversation: {
        en: string;
        zh: string;
    };
};

export default function DailyPage() {
    const router = useRouter();

    const [data, setData] = useState<DailyData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`${API_BASE_URL}/api/daily`)
            .then((res) => res.json())
            .then((json) => {
                setData(json.data);
                setLoading(false);
            })
            .catch(() => {
                setLoading(false);
            });
    }, []);

    return (
        <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
            <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 20 }}>
                今日學習 {data?.level && `（${data.level}）`}
            </h1>

            {loading && <p>載入中...</p>}

            {data && (
                <>
                    {/* 單字 */}
                    <div style={card}>
                        <h2>今日 5 個單字</h2>

                        {data.vocabulary.map((item, index) => (
                            <div key={index} style={row}>
                                <strong>{item.word}</strong>
                                <span>{item.meaning}</span>
                            </div>
                        ))}
                    </div>

                    {/* 會話 */}
                    <div style={card}>
                        <h2>今日會話</h2>
                        <p style={{ fontSize: 18 }}>{data.conversation.en}</p>
                        <p style={{ color: "#666" }}>{data.conversation.zh}</p>
                    </div>

                    {/* 練習 */}
                    <div
                        style={{ ...card, background: "#eef2ff", cursor: "pointer" }}
                        onClick={() => router.push("/chat")}
                    >
                        <h2>開始練習</h2>
                        <p>用今天內容進行對話</p>
                    </div>
                </>
            )}
        </main>
    );
}

const card: React.CSSProperties = {
    border: "1px solid #ddd",
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    background: "#fff",
};

const row: React.CSSProperties = {
    display: "flex",
    justifyContent: "space-between",
    padding: "6px 0",
};
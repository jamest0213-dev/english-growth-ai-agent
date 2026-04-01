"use client";

import { useState } from "react";

type ChatResult = {
    mode: string;
    correct: string;
    explanation: string;
    suggestion: string;
    cefr_level: string;
};

const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function ChatPage() {
    const [message, setMessage] = useState("");
    const [result, setResult] = useState<ChatResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const handleSubmit = async () => {
        if (!message.trim()) {
            setErrorMessage("請先輸入英文句子");
            return;
        }

        setLoading(true);
        setErrorMessage("");
        setResult(null);

        try {
            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message,
                }),
            });

            if (!response.ok) {
                throw new Error("API 回應失敗");
            }

            const data = await response.json();
            setResult(data.data);
        } catch (error) {
            setErrorMessage("系統暫時無法連線，請稍後再試");
        } finally {
            setLoading(false);
        }
    };

    return (
        <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
            <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 20 }}>
                對話模式
            </h1>

            <div
                style={{
                    border: "1px solid #ddd",
                    borderRadius: 12,
                    padding: 16,
                    marginBottom: 20,
                    background: "#fff",
                }}
            >
                <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    rows={5}
                    placeholder="例如：I go to school yesterday."
                    style={{
                        width: "100%",
                        border: "1px solid #ccc",
                        borderRadius: 8,
                        padding: 12,
                        fontSize: 16,
                    }}
                />

                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    style={{
                        marginTop: 12,
                        padding: "10px 16px",
                        borderRadius: 8,
                        border: "none",
                        background: "#111827",
                        color: "#fff",
                    }}
                >
                    {loading ? "分析中..." : "送出分析"}
                </button>

                {errorMessage && (
                    <p style={{ color: "red", marginTop: 10 }}>{errorMessage}</p>
                )}
            </div>

            {result && (
                <div
                    style={{
                        border: "1px solid #ddd",
                        borderRadius: 12,
                        padding: 16,
                        background: "#fafafa",
                    }}
                >
                    <h2>分析結果</h2>

                    <p><strong>CEFR：</strong>{result.cefr_level}</p>

                    {result.mode === "mock" && (
                        <p style={{ color: "orange" }}>目前為模擬模式</p>
                    )}

                    <p><strong>Correct：</strong>{result.correct}</p>
                    <p><strong>說明：</strong>{result.explanation}</p>
                    <p><strong>Suggestion：</strong>{result.suggestion}</p>
                </div>
            )}
        </main>
    );
}
'use client';

import { FormEvent, useMemo, useState } from 'react';

type TabKey = 'dashboard' | 'chat' | 'vocab' | 'writing' | 'speaking' | 'analysis';

type ToastItem = {
  id: number;
  title: string;
  message: string;
};

const tabs: Array<{ key: TabKey; label: string }> = [
  { key: 'dashboard', label: '主頁總覽' },
  { key: 'chat', label: '對話學習' },
  { key: 'vocab', label: '單字學習' },
  { key: 'writing', label: '寫作訓練' },
  { key: 'speaking', label: '口說訓練' },
  { key: 'analysis', label: '進度分析' },
];

const vocabularyDeck = [
  { word: 'resilient', meaning: '有韌性的', example: 'She stayed resilient during the interview challenge.' },
  { word: 'itinerary', meaning: '行程表', example: 'Our travel itinerary includes a museum visit.' },
  { word: 'collaborate', meaning: '合作', example: 'Team members collaborate to solve problems quickly.' },
];

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<TabKey>('dashboard');
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const pushToast = (title: string, message: string) => {
    setToasts((prev) => [...prev, { id: Date.now(), title, message }]);
  };

  const closeToast = (id: number) => setToasts((prev) => prev.filter((toast) => toast.id !== id));

  return (
    <main className="min-h-screen bg-app-bg px-4 py-8 text-slate-900">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6">
        <header className="rounded-2xl bg-primary px-6 py-5 text-white shadow-lg">
          <h1 className="text-2xl font-bold">English Growth AI Agent</h1>
          <p className="mt-2 text-sm text-blue-100">以 CEFR 成長為核心的英語學習儀表板</p>
        </header>

        <nav className="grid grid-cols-2 gap-2 rounded-2xl bg-white p-2 shadow md:grid-cols-6">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              className={`rounded-xl px-3 py-2 text-sm font-medium transition ${
                activeTab === tab.key ? 'bg-primary text-white' : 'bg-slate-100 hover:bg-slate-200'
              }`}
              onClick={() => setActiveTab(tab.key)}
              type="button"
            >
              {tab.label}
            </button>
          ))}
        </nav>

        <section className="rounded-2xl bg-white p-6 shadow">
          {activeTab === 'dashboard' && <DashboardSection />}
          {activeTab === 'chat' && <ChatSection pushToast={pushToast} />}
          {activeTab === 'vocab' && <VocabularySection pushToast={pushToast} />}
          {activeTab === 'writing' && <WritingSection pushToast={pushToast} />}
          {activeTab === 'speaking' && <SpeakingSection pushToast={pushToast} />}
          {activeTab === 'analysis' && <AnalysisSection />}
        </section>
      </div>

      <div className="fixed bottom-4 right-4 z-50 flex w-80 flex-col gap-3">
        {toasts.map((toast) => (
          <div key={toast.id} className="rounded-xl border border-slate-200 bg-white p-3 shadow-lg">
            <div className="mb-1 flex items-center justify-between">
              <h3 className="font-semibold text-primary">{toast.title}</h3>
              <button className="text-xs text-slate-500" onClick={() => closeToast(toast.id)} type="button">
                關閉
              </button>
            </div>
            <p className="text-sm text-slate-700">{toast.message}</p>
            <button
              className="mt-2 rounded bg-accent px-2 py-1 text-xs font-semibold text-slate-900"
              onClick={() => navigator.clipboard.writeText(toast.message)}
              type="button"
            >
              複製內容
            </button>
          </div>
        ))}
      </div>
    </main>
  );
}

function DashboardSection() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-primary">今日學習進度</h2>
      <div className="grid gap-4 md:grid-cols-3">
        <InfoCard title="今日完成率" value="75%" detail="已完成 3/4 任務" />
        <InfoCard title="目前 CEFR" value="B1" detail="距離 B2 還差 12 分" />
        <InfoCard title="連續學習" value="8 天" detail="保持節奏很棒！" />
      </div>
      <div>
        <h3 className="mb-2 font-semibold">成長曲線（近 7 天）</h3>
        <div className="flex h-36 items-end gap-2 rounded-xl bg-slate-50 p-4">
          {[45, 50, 52, 58, 62, 65, 72].map((score, index) => (
            <div key={score} className="flex flex-1 flex-col items-center gap-1">
              <div className="w-full rounded-t bg-primary" style={{ height: `${score}%` }} />
              <span className="text-xs text-slate-500">D{index + 1}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ChatSection({ pushToast }: { pushToast: (title: string, message: string) => void }) {
  const [role, setRole] = useState('teacher');
  const [message, setMessage] = useState('I goed to school yesterday.');
  const [streamingText, setStreamingText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const roleLabel = useMemo(
    () => ({ teacher: '老師', interviewer: '面試官', travel: '旅遊情境' }[role] ?? '老師'),
    [role],
  );

  const startStreaming = async (event: FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    setStreamingText('');

    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';
    try {
      const response = await fetch(`${baseUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: `[${roleLabel}] ${message}`, provider: 'mock' }),
      });

      if (!response.body) {
        throw new Error('無法取得串流內容');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
      while (!done) {
        const result = await reader.read();
        done = result.done;
        const chunk = decoder.decode(result.value || new Uint8Array(), { stream: true });
        const lines = chunk.split('\n').filter((line) => line.startsWith('data: '));

        lines.forEach((line) => {
          const payloadText = line.replace('data: ', '').trim();
          if (!payloadText) return;
          const payload = JSON.parse(payloadText) as { type: string; content?: string; message?: string };
          if (payload.type === 'chunk' && payload.content) {
            setStreamingText((prev) => prev + payload.content);
          }
          if (payload.type === 'warning' && payload.message) {
            pushToast('系統提醒', payload.message);
          }
        });
      }
    } catch (error) {
      pushToast('串流失敗', '目前無法連線到後端，已保留輸入內容。');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold text-primary">對話學習頁（Streaming）</h2>
      <form className="space-y-3" onSubmit={startStreaming}>
        <select className="w-full rounded-lg border p-2" onChange={(e) => setRole(e.target.value)} value={role}>
          <option value="teacher">老師</option>
          <option value="interviewer">面試官</option>
          <option value="travel">旅遊情境</option>
        </select>
        <textarea className="h-24 w-full rounded-lg border p-3" onChange={(e) => setMessage(e.target.value)} value={message} />
        <button className="rounded-lg bg-primary px-4 py-2 font-semibold text-white" disabled={isLoading} type="submit">
          {isLoading ? '串流回應中...' : '開始練習'}
        </button>
      </form>

      <div className="rounded-xl bg-slate-50 p-4">
        <p>
          <strong>修正句：</strong>
          {streamingText || '尚未產生'}
        </p>
        <p className="mt-2">
          <strong>評分：</strong>78 / 100
        </p>
        <p className="mt-2">
          <strong>建議：</strong>多使用過去式動詞並加入連接詞，讓句子更自然。
        </p>
      </div>
    </div>
  );
}

function VocabularySection({ pushToast }: { pushToast: (title: string, message: string) => void }) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);

  const card = vocabularyDeck[index];

  const pronounce = () => {
    const utterance = new SpeechSynthesisUtterance(card.word);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
    pushToast('發音播放', `正在播放 ${card.word} 的發音。`);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold text-primary">單字學習頁</h2>
      <button className="w-full rounded-xl border-2 border-primary p-8 text-center" onClick={() => setFlipped(!flipped)} type="button">
        <p className="text-sm text-slate-500">點擊翻轉單字卡</p>
        <p className="mt-2 text-2xl font-bold">{flipped ? card.meaning : card.word}</p>
      </button>
      <p>
        <strong>例句：</strong> {card.example}
      </p>
      <div className="flex gap-2">
        <button className="rounded bg-primary px-4 py-2 text-white" onClick={pronounce} type="button">
          發音
        </button>
        <button
          className="rounded bg-slate-200 px-4 py-2"
          onClick={() => {
            setIndex((prev) => (prev + 1) % vocabularyDeck.length);
            setFlipped(false);
          }}
          type="button"
        >
          下一張
        </button>
      </div>
    </div>
  );
}

function WritingSection({ pushToast }: { pushToast: (title: string, message: string) => void }) {
  const [essay, setEssay] = useState('I think online learning is good because it is flexible.');
  const [result, setResult] = useState('尚未批改');
  const [loading, setLoading] = useState(false);

  const reviewEssay = async () => {
    setLoading(true);
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';
    try {
      const response = await fetch(`${baseUrl}/api/chat/complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: `請進行寫作批改，提供 Grammar 與 Style 建議：${essay}`,
          provider: 'mock',
        }),
      });
      const data = (await response.json()) as { content?: string };
      setResult(data.content ?? '暫時無法取得批改結果');
    } catch {
      pushToast('批改失敗', '目前無法連線後端，請稍後再試。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-3">
      <h2 className="text-xl font-bold text-primary">寫作訓練頁</h2>
      <textarea className="h-40 w-full rounded-lg border p-3" onChange={(e) => setEssay(e.target.value)} value={essay} />
      <button className="rounded bg-primary px-4 py-2 text-white" disabled={loading} onClick={reviewEssay} type="button">
        {loading ? '批改中...' : 'AI 批改（Grammar + Style）'}
      </button>
      <div className="rounded-xl bg-slate-50 p-3">
        <strong>批改結果：</strong>
        <p className="mt-2 whitespace-pre-wrap">{result}</p>
      </div>
    </div>
  );
}

function SpeakingSection({ pushToast }: { pushToast: (title: string, message: string) => void }) {
  const [recording, setRecording] = useState(false);
  const [spokenText, setSpokenText] = useState('Today I want to describe my daily routine.');
  const [feedback, setFeedback] = useState('尚未分析');

  const toggleRecording = () => {
    setRecording((prev) => !prev);
    pushToast('錄音功能', '示範版已切換錄音狀態，可直接送出文字進行評估。');
  };

  const getSpeakingFeedback = async () => {
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';
    try {
      const response = await fetch(`${baseUrl}/api/speaking`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: spokenText, cefr_level: 'B1', provider: 'mock', enable_tts: false }),
      });
      const data = (await response.json()) as { feedback?: string; pronunciation_score?: number };
      setFeedback(`即時回饋：${data.feedback ?? '無資料'}\n發音建議分數：${data.pronunciation_score ?? '-'} / 100`);
    } catch {
      pushToast('口說失敗', '目前無法取得口說回饋，請稍後再試。');
    }
  };

  return (
    <div className="space-y-3">
      <h2 className="text-xl font-bold text-primary">口說訓練頁</h2>
      <div className="flex gap-2">
        <button className="rounded bg-primary px-4 py-2 text-white" onClick={toggleRecording} type="button">
          {recording ? '停止錄音' : '開始錄音'}
        </button>
        <span className="self-center text-sm text-slate-600">目前狀態：{recording ? '錄音中' : '待機'}</span>
      </div>
      <textarea className="h-24 w-full rounded-lg border p-3" onChange={(e) => setSpokenText(e.target.value)} value={spokenText} />
      <button className="rounded bg-slate-800 px-4 py-2 text-white" onClick={getSpeakingFeedback} type="button">
        取得即時回饋
      </button>
      <pre className="rounded-xl bg-slate-50 p-3 text-sm whitespace-pre-wrap">{feedback}</pre>
    </div>
  );
}

function AnalysisSection() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold text-primary">進度分析頁</h2>
      <div className="grid gap-4 md:grid-cols-3">
        <InfoCard title="CEFR 成長" value="A2 → B1" detail="近 30 天提升 1 個級距" />
        <InfoCard title="錯誤類型統計" value="時態 40%" detail="其次為冠詞 25%" />
        <InfoCard title="學習時間" value="12.5 小時" detail="平均每日 25 分鐘" />
      </div>
    </div>
  );
}

function InfoCard({ title, value, detail }: { title: string; value: string; detail: string }) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="text-sm text-slate-500">{title}</h3>
      <p className="mt-2 text-2xl font-bold text-primary">{value}</p>
      <p className="mt-1 text-sm text-slate-600">{detail}</p>
    </article>
  );
}

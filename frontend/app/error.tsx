'use client';

import { useEffect } from 'react';

type ErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('App route error:', error);
  }, [error]);

  return (
    <main className="flex min-h-screen items-center justify-center bg-app-bg px-4">
      <div className="w-full max-w-lg rounded-2xl bg-white p-6 text-center shadow">
        <h2 className="text-2xl font-bold text-primary">頁面暫時發生問題</h2>
        <p className="mt-3 text-sm text-slate-700">系統已攔截錯誤，請按下方按鈕重新載入畫面。</p>
        <button
          className="mt-5 rounded-lg bg-primary px-4 py-2 font-semibold text-white"
          onClick={reset}
          type="button"
        >
          重新載入
        </button>
      </div>
    </main>
  );
}

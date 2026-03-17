'use client';

import { useEffect } from 'react';

type GlobalErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function GlobalError({ error, reset }: GlobalErrorProps) {
  useEffect(() => {
    console.error('Global app error:', error);
  }, [error]);

  return (
    <html lang="zh-Hant">
      <body className="bg-app-bg">
        <main className="flex min-h-screen items-center justify-center px-4">
          <div className="w-full max-w-lg rounded-2xl bg-white p-6 text-center shadow">
            <h2 className="text-2xl font-bold text-primary">系統發生錯誤</h2>
            <p className="mt-3 text-sm text-slate-700">請點擊重新整理按鈕，系統會自動嘗試恢復。</p>
            <button
              className="mt-5 rounded-lg bg-primary px-4 py-2 font-semibold text-white"
              onClick={reset}
              type="button"
            >
              重新整理
            </button>
          </div>
        </main>
      </body>
    </html>
  );
}

'use client';

import { useEffect, useState } from 'react';

export default function HomePage() {
  const [health, setHealth] = useState('checking...');

  useEffect(() => {
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

    fetch(`${baseUrl}/healthz`)
      .then((response) => response.json())
      .then((data) => setHealth(data.status ?? 'unknown'))
      .catch(() => setHealth('unreachable'));
  }, []);

  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col items-center justify-center gap-4 p-6">
      <h1 className="text-3xl font-bold">English Growth AI Agent MVP</h1>
      <p className="text-lg">Stage 0 scaffold is running.</p>
      <div className="rounded-md bg-white px-4 py-2 shadow">API health: {health}</div>
    </main>
  );
}

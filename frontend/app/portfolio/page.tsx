"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Item = { title: string; tag: string; image_url: string };

export default function PortfolioPage() {
  const [items, setItems] = useState<Item[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/api/content/portfolio`)
      .then((r) => r.json())
      .then(setItems);
  }, []);

  return (
    <main className="px-6 md:px-12 py-16 max-w-5xl mx-auto">
      <h1 className="font-display text-4xl mb-10">Recent work</h1>
      <div className="grid md:grid-cols-3 gap-6">
        {items.map((p, i) => (
          <div
            key={i}
            className="rounded-2xl border border-stone/20 aspect-square flex flex-col justify-end bg-grout text-porcelain overflow-hidden relative"
          >
            {p.image_url && (
              /* eslint-disable-next-line @next/next/no-img-element */
              <img
                src={p.image_url}
                alt={p.title}
                className="absolute inset-0 w-full h-full object-cover opacity-70"
              />
            )}
            <div className="relative p-6">
              <h3 className="font-medium">{p.title}</h3>
              <p className="text-xs text-porcelain/60 mt-1">{p.tag}</p>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}

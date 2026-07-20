"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type ReviewItem = { text: string; author: string };

export default function ReviewsPage() {
  const [reviews, setReviews] = useState<ReviewItem[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/api/content/reviews`)
      .then((r) => r.json())
      .then(setReviews);
  }, []);

  return (
    <main className="px-6 md:px-12 py-16 max-w-3xl mx-auto">
      <h1 className="font-display text-4xl mb-10">What customers say</h1>
      <div className="space-y-6">
        {reviews.map((r, i) => (
          <blockquote key={i} className="border-l-2 border-glaze pl-4 text-stone">
            "{r.text}"
            <footer className="text-xs mt-2 text-grout/60">— {r.author}</footer>
          </blockquote>
        ))}
      </div>
    </main>
  );
}

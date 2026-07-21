"use client";

import { useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function AccentColorLoader() {
  useEffect(() => {
    fetch(`${API_URL}/api/content/site`)
      .then((r) => r.json())
      .then((data) => {
        if (data.accent_color) {
          document.documentElement.style.setProperty("--accent", data.accent_color);
        }
      })
      .catch(() => {});
  }, []);

  return null;
}

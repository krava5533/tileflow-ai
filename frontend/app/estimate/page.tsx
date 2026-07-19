"use client";

import { useState, useRef } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Message = { role: "user" | "assistant"; content: string };

export default function EstimatePage() {
  const [leadId, setLeadId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hi! I'm Tila. What's your name and phone number, and what project are you working on?" },
  ]);
  const [input, setInput] = useState("");
  const [estimate, setEstimate] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  async function ensureLead(): Promise<string> {
    if (leadId) return leadId;
    const res = await fetch(`${API_URL}/api/leads`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        customer: { name: "Website Visitor", phone: "unknown" },
        source: "website_ai_chat",
      }),
    });
    const data = await res.json();
    setLeadId(data.lead_id);
    return data.lead_id;
  }

  async function sendMessage() {
    if (!input.trim()) return;
    const text = input;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }]);
    setLoading(true);
    try {
      const id = await ensureLead();
      const res = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lead_id: id, message: text }),
      });
      const data = await res.json();
      setMessages((m) => [...m, { role: "assistant", content: data.reply }]);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpload() {
    const file = fileRef.current?.files?.[0];
    if (!file) return;
    setLoading(true);
    try {
      const id = await ensureLead();
      const form = new FormData();
      form.append("lead_id", id);
      form.append("file", file);
      const res = await fetch(`${API_URL}/api/uploads`, { method: "POST", body: form });
      const data = await res.json();
      setMessages((m) => [
        ...m,
        { role: "user", content: `[uploaded photo: ${file.name}]` },
        {
          role: "assistant",
          content: `Thanks! Looks like a ${data.analysis?.room_type ?? "project"} at roughly ${data.analysis?.estimated_sqft ?? "?"} sq ft. Want me to generate your estimate now?`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function generateEstimate() {
    if (!leadId) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/estimates/${leadId}/generate`, { method: "POST" });
      const data = await res.json();
      setEstimate(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-porcelain px-6 md:px-12 py-12 max-w-2xl mx-auto">
      <h1 className="font-display text-3xl mb-2">Get your free AI estimate</h1>
      <p className="text-stone mb-8 text-sm">
        Chat with Tila, upload a photo or two, and get a preliminary number in minutes.
      </p>

      <div className="bg-grout rounded-2xl p-5 space-y-3 mb-4 min-h-[300px]">
        {messages.map((m, i) => (
          <div
            key={i}
            className={
              "rounded-xl px-4 py-3 text-sm w-fit max-w-[85%] " +
              (m.role === "assistant"
                ? "bg-porcelain/10 text-porcelain rounded-tl-sm"
                : "bg-glaze text-porcelain rounded-tr-sm ml-auto")
            }
          >
            {m.content}
          </div>
        ))}
        {loading && <div className="text-porcelain/50 text-xs">Tila is typing…</div>}
      </div>

      <div className="flex gap-2 mb-4">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your reply…"
          className="flex-1 border border-stone/30 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-glaze"
        />
        <button
          onClick={sendMessage}
          className="px-5 py-2 rounded-full bg-grout text-porcelain text-sm hover:bg-glaze transition-colors"
        >
          Send
        </button>
      </div>

      <div className="flex items-center gap-4 mb-8">
        <input ref={fileRef} type="file" accept="image/*" className="text-sm" />
        <button
          onClick={handleUpload}
          className="px-4 py-2 rounded-full border border-grout text-sm hover:bg-grout hover:text-porcelain transition-colors"
        >
          Upload photo
        </button>
        <button
          onClick={generateEstimate}
          disabled={!leadId}
          className="px-4 py-2 rounded-full bg-clay text-porcelain text-sm disabled:opacity-40"
        >
          Generate estimate
        </button>
      </div>

      {estimate && (
        <div className="border border-stone/30 rounded-2xl p-6">
          <h2 className="font-display text-xl mb-4">Preliminary estimate</h2>
          <dl className="text-sm space-y-2">
            <div className="flex justify-between"><dt className="text-stone">Materials</dt><dd>${estimate.materials_cost} CAD</dd></div>
            <div className="flex justify-between"><dt className="text-stone">Labor</dt><dd>${estimate.labor_cost} CAD</dd></div>
            <div className="flex justify-between"><dt className="text-stone">Demo / prep / waterproofing</dt><dd>${estimate.demolition_cost} CAD</dd></div>
            <div className="flex justify-between"><dt className="text-stone">Subtotal</dt><dd>${estimate.subtotal} CAD</dd></div>
            <div className="flex justify-between"><dt className="text-stone">Tax ({Math.round(estimate.tax_rate * 100)}%)</dt><dd>${estimate.tax_amount} CAD</dd></div>
            <div className="flex justify-between font-medium text-base pt-2 border-t border-stone/20">
              <dt>Total</dt><dd>${estimate.total_cost} CAD</dd>
            </div>
          </dl>
          {estimate.pdf_url && (
            <a
              href={estimate.pdf_url}
              target="_blank"
              className="inline-block mt-4 text-sm text-glaze underline"
            >
              Download PDF estimate →
            </a>
          )}
        </div>
      )}
    </main>
  );
}

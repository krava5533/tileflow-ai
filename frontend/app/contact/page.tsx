"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ContactPage() {
  const [contact, setContact] = useState<{ contact_phone: string; contact_email: string } | null>(null);

  useEffect(() => {
    fetch(`${API_URL}/api/content/site`)
      .then((r) => r.json())
      .then(setContact)
      .catch(() => {});
  }, []);

  return (
    <main className="px-6 md:px-12 py-16 max-w-lg mx-auto">
      <h1 className="font-display text-4xl mb-6">Contact us</h1>
      <p className="text-stone mb-4 text-sm">
        Prefer talking to a person first? Reach out directly — or use the AI estimate
        tool for the fastest response.
      </p>
      {(contact?.contact_phone || contact?.contact_email) && (
        <div className="mb-8 text-sm space-y-1">
          {contact.contact_phone && <p>📞 {contact.contact_phone}</p>}
          {contact.contact_email && <p>✉️ {contact.contact_email}</p>}
        </div>
      )}
      <form className="space-y-4">
        <input className="w-full border border-stone/30 rounded-full px-4 py-2 text-sm" placeholder="Name" />
        <input className="w-full border border-stone/30 rounded-full px-4 py-2 text-sm" placeholder="Phone" />
        <textarea className="w-full border border-stone/30 rounded-2xl px-4 py-2 text-sm" placeholder="Message" rows={4} />
        <button
          type="submit"
          className="px-6 py-2 rounded-full bg-grout text-porcelain text-sm transition-colors"
          style={{ backgroundColor: "var(--accent)" }}
        >
          Send
        </button>
      </form>
    </main>
  );
}

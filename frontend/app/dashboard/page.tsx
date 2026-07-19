"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const STATUSES = [
  "new_lead",
  "contacted",
  "estimate_scheduled",
  "estimate_sent",
  "approved",
  "completed",
];

const STATUS_LABELS: Record<string, string> = {
  new_lead: "New Lead",
  contacted: "Contacted",
  estimate_scheduled: "Estimate Scheduled",
  estimate_sent: "Estimate Sent",
  approved: "Approved",
  completed: "Completed",
};

type Lead = {
  id: string;
  status: string;
  project_type: string;
  customer_name: string;
  customer_phone: string;
  created_at: string;
};

export default function DashboardPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [filter, setFilter] = useState<string>("");
  const [loading, setLoading] = useState(true);

  async function loadLeads() {
    setLoading(true);
    const url = filter ? `${API_URL}/api/leads?status=${filter}` : `${API_URL}/api/leads`;
    const res = await fetch(url);
    const data = await res.json();
    setLeads(data);
    setLoading(false);
  }

  useEffect(() => {
    loadLeads();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  async function updateStatus(id: string, status: string) {
    await fetch(`${API_URL}/api/leads/${id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    loadLeads();
  }

  return (
    <main className="min-h-screen bg-porcelain px-6 md:px-12 py-10">
      <div className="flex items-center justify-between mb-8">
        <h1 className="font-display text-3xl">Lead Dashboard</h1>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="border border-stone/30 rounded-full px-4 py-2 text-sm"
        >
          <option value="">All statuses</option>
          {STATUSES.map((s) => (
            <option key={s} value={s}>{STATUS_LABELS[s]}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <p className="text-stone text-sm">Loading…</p>
      ) : leads.length === 0 ? (
        <p className="text-stone text-sm">No leads yet — they'll show up here as customers come in through the AI Estimate flow.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="text-left text-stone border-b border-stone/20">
                <th className="py-3 pr-4">Customer</th>
                <th className="py-3 pr-4">Phone</th>
                <th className="py-3 pr-4">Project</th>
                <th className="py-3 pr-4">Received</th>
                <th className="py-3 pr-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((lead) => (
                <tr key={lead.id} className="border-b border-stone/10">
                  <td className="py-3 pr-4">{lead.customer_name || "—"}</td>
                  <td className="py-3 pr-4">{lead.customer_phone || "—"}</td>
                  <td className="py-3 pr-4 capitalize">{lead.project_type?.replace("_", " ")}</td>
                  <td className="py-3 pr-4 text-stone">
                    {lead.created_at ? new Date(lead.created_at).toLocaleDateString("en-CA") : "—"}
                  </td>
                  <td className="py-3 pr-4">
                    <select
                      value={lead.status}
                      onChange={(e) => updateStatus(lead.id, e.target.value)}
                      className="border border-stone/30 rounded-full px-3 py-1 text-xs"
                    >
                      {STATUSES.map((s) => (
                        <option key={s} value={s}>{STATUS_LABELS[s]}</option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}

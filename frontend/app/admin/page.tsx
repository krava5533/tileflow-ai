"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type PriceBook = {
  material_cost_per_sqft: Record<string, number>;
  labor_cost_per_sqft: Record<string, number>;
  demolition_cost_per_sqft: number;
  waterproofing_cost_per_sqft: number;
  default_province: string;
};

type PortfolioItem = { title: string; tag: string; image_url: string };
type ReviewItem = { text: string; author: string };
type SiteContent = {
  hero_title_line1: string;
  hero_title_line2: string;
  hero_subtitle: string;
  contact_phone: string;
  contact_email: string;
  accent_color: string;
};

export default function AdminPage() {
  const [password, setPassword] = useState("");
  const [authed, setAuthed] = useState(false);
  const [loginError, setLoginError] = useState("");
  const [priceBook, setPriceBook] = useState<PriceBook | null>(null);
  const [portfolio, setPortfolio] = useState<PortfolioItem[]>([]);
  const [reviews, setReviews] = useState<ReviewItem[]>([]);
  const [siteContent, setSiteContent] = useState<SiteContent | null>(null);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const stored = sessionStorage.getItem("tileflow_admin_password");
    if (stored) {
      setPassword(stored);
      tryLogin(stored);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function tryLogin(pw: string) {
    setLoginError("");
    const res = await fetch(`${API_URL}/api/admin/login`, {
      method: "POST",
      headers: { "X-Admin-Password": pw },
    });
    if (!res.ok) {
      setLoginError("Wrong password");
      setAuthed(false);
      return;
    }
    sessionStorage.setItem("tileflow_admin_password", pw);
    setAuthed(true);
    loadPriceBook(pw);
  }

  async function loadPriceBook(pw: string) {
    const res = await fetch(`${API_URL}/api/admin/price-book`, {
      headers: { "X-Admin-Password": pw },
    });
    const data = await res.json();
    setPriceBook(data);

    const portfolioRes = await fetch(`${API_URL}/api/admin/portfolio`, {
      headers: { "X-Admin-Password": pw },
    });
    setPortfolio(await portfolioRes.json());

    const reviewsRes = await fetch(`${API_URL}/api/admin/reviews`, {
      headers: { "X-Admin-Password": pw },
    });
    setReviews(await reviewsRes.json());

    const siteRes = await fetch(`${API_URL}/api/admin/site-content`, {
      headers: { "X-Admin-Password": pw },
    });
    setSiteContent(await siteRes.json());
  }

  async function save() {
    if (!priceBook) return;
    setSaving(true);
    setSaved(false);
    try {
      await fetch(`${API_URL}/api/admin/price-book`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", "X-Admin-Password": password },
        body: JSON.stringify(priceBook),
      });
      await fetch(`${API_URL}/api/admin/portfolio`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", "X-Admin-Password": password },
        body: JSON.stringify(portfolio),
      });
      await fetch(`${API_URL}/api/admin/reviews`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", "X-Admin-Password": password },
        body: JSON.stringify(reviews),
      });
      await fetch(`${API_URL}/api/admin/site-content`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", "X-Admin-Password": password },
        body: JSON.stringify(siteContent),
      });
      setSaved(true);
    } finally {
      setSaving(false);
    }
  }

  function updatePortfolioItem(index: number, field: keyof PortfolioItem, value: string) {
    setPortfolio(portfolio.map((item, i) => (i === index ? { ...item, [field]: value } : item)));
  }

  function addPortfolioItem() {
    setPortfolio([...portfolio, { title: "", tag: "", image_url: "" }]);
  }

  function removePortfolioItem(index: number) {
    setPortfolio(portfolio.filter((_, i) => i !== index));
  }

  function updateReviewItem(index: number, field: keyof ReviewItem, value: string) {
    setReviews(reviews.map((item, i) => (i === index ? { ...item, [field]: value } : item)));
  }

  function addReviewItem() {
    setReviews([...reviews, { text: "", author: "" }]);
  }

  function removeReviewItem(index: number) {
    setReviews(reviews.filter((_, i) => i !== index));
  }

  function updateMaterial(key: string, value: string) {
    if (!priceBook) return;
    setPriceBook({
      ...priceBook,
      material_cost_per_sqft: { ...priceBook.material_cost_per_sqft, [key]: parseFloat(value) || 0 },
    });
  }

  function updateLabor(key: string, value: string) {
    if (!priceBook) return;
    setPriceBook({
      ...priceBook,
      labor_cost_per_sqft: { ...priceBook.labor_cost_per_sqft, [key]: parseFloat(value) || 0 },
    });
  }

  if (!authed) {
    return (
      <main className="min-h-screen bg-porcelain flex items-center justify-center px-6">
        <div className="max-w-sm w-full">
          <h1 className="font-display text-2xl mb-4">Admin login</h1>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && tryLogin(password)}
            placeholder="Admin password"
            className="w-full border border-stone/30 rounded-full px-4 py-2 text-sm mb-3"
          />
          {loginError && <p className="text-sm text-red-600 mb-3">{loginError}</p>}
          <button
            onClick={() => tryLogin(password)}
            className="w-full px-4 py-2 rounded-full bg-grout text-porcelain text-sm hover:bg-glaze transition-colors"
          >
            Log in
          </button>
        </div>
      </main>
    );
  }

  if (!priceBook || !siteContent) {
    return <main className="min-h-screen bg-porcelain px-6 py-12">Loading…</main>;
  }

  return (
    <main className="min-h-screen bg-porcelain px-6 md:px-12 py-10 max-w-2xl mx-auto">
      <h1 className="font-display text-3xl mb-8">Site settings</h1>

      <section className="mb-8">
        <h2 className="font-medium mb-3">Homepage & branding</h2>
        <div className="space-y-3">
          <label className="text-sm block">
            <span className="block text-stone mb-1">Hero title, line 1</span>
            <input
              value={siteContent?.hero_title_line1 || ""}
              onChange={(e) => setSiteContent({ ...(siteContent as SiteContent), hero_title_line1: e.target.value })}
              className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
            />
          </label>
          <label className="text-sm block">
            <span className="block text-stone mb-1">Hero title, line 2</span>
            <input
              value={siteContent?.hero_title_line2 || ""}
              onChange={(e) => setSiteContent({ ...(siteContent as SiteContent), hero_title_line2: e.target.value })}
              className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
            />
          </label>
          <label className="text-sm block">
            <span className="block text-stone mb-1">Hero subtitle</span>
            <textarea
              value={siteContent?.hero_subtitle || ""}
              onChange={(e) => setSiteContent({ ...(siteContent as SiteContent), hero_subtitle: e.target.value })}
              rows={3}
              className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
            />
          </label>
          <div className="grid grid-cols-2 gap-3">
            <label className="text-sm block">
              <span className="block text-stone mb-1">Contact phone</span>
              <input
                value={siteContent?.contact_phone || ""}
                onChange={(e) => setSiteContent({ ...(siteContent as SiteContent), contact_phone: e.target.value })}
                className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
              />
            </label>
            <label className="text-sm block">
              <span className="block text-stone mb-1">Contact email</span>
              <input
                value={siteContent?.contact_email || ""}
                onChange={(e) => setSiteContent({ ...(siteContent as SiteContent), contact_email: e.target.value })}
                className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
              />
            </label>
          </div>
          <label className="text-sm block">
            <span className="block text-stone mb-1">Accent color (buttons, highlights)</span>
            <div className="flex items-center gap-3">
              <input
                type="color"
                value={siteContent?.accent_color || "#3F6E64"}
                onChange={(e) => setSiteContent({ ...(siteContent as SiteContent), accent_color: e.target.value })}
                className="h-10 w-16 border border-stone/30 rounded-lg"
              />
              <span className="text-stone">{siteContent?.accent_color}</span>
            </div>
          </label>
        </div>
      </section>

      <section className="mb-8">
        <h2 className="font-medium mb-3">Material cost per sq ft (CAD)</h2>
        <div className="grid grid-cols-2 gap-3">
          {Object.entries(priceBook.material_cost_per_sqft).map(([key, value]) => (
            <label key={key} className="text-sm">
              <span className="block text-stone capitalize mb-1">{key.replace("_", " ")}</span>
              <input
                type="number"
                step="0.01"
                value={value}
                onChange={(e) => updateMaterial(key, e.target.value)}
                className="w-full border border-stone/30 rounded-lg px-3 py-2"
              />
            </label>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="font-medium mb-3">Labor cost per sq ft (CAD), by complexity</h2>
        <div className="grid grid-cols-3 gap-3">
          {Object.entries(priceBook.labor_cost_per_sqft).map(([key, value]) => (
            <label key={key} className="text-sm">
              <span className="block text-stone capitalize mb-1">{key}</span>
              <input
                type="number"
                step="0.01"
                value={value}
                onChange={(e) => updateLabor(key, e.target.value)}
                className="w-full border border-stone/30 rounded-lg px-3 py-2"
              />
            </label>
          ))}
        </div>
      </section>

      <section className="mb-8 grid grid-cols-2 gap-3">
        <label className="text-sm">
          <span className="block text-stone mb-1">Demolition / sq ft (CAD)</span>
          <input
            type="number"
            step="0.01"
            value={priceBook.demolition_cost_per_sqft}
            onChange={(e) =>
              setPriceBook({ ...priceBook, demolition_cost_per_sqft: parseFloat(e.target.value) || 0 })
            }
            className="w-full border border-stone/30 rounded-lg px-3 py-2"
          />
        </label>
        <label className="text-sm">
          <span className="block text-stone mb-1">Waterproofing / sq ft (CAD)</span>
          <input
            type="number"
            step="0.01"
            value={priceBook.waterproofing_cost_per_sqft}
            onChange={(e) =>
              setPriceBook({ ...priceBook, waterproofing_cost_per_sqft: parseFloat(e.target.value) || 0 })
            }
            className="w-full border border-stone/30 rounded-lg px-3 py-2"
          />
        </label>
      </section>

      <section className="mb-8">
        <h2 className="font-medium mb-3">Portfolio</h2>
        <div className="space-y-4">
          {portfolio.map((item, i) => (
            <div key={i} className="border border-stone/20 rounded-xl p-4 space-y-2">
              <input
                placeholder="Title (e.g. Master Bath Remodel)"
                value={item.title}
                onChange={(e) => updatePortfolioItem(i, "title", e.target.value)}
                className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
              />
              <input
                placeholder="Tag (e.g. Bathroom · Porcelain)"
                value={item.tag}
                onChange={(e) => updatePortfolioItem(i, "tag", e.target.value)}
                className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
              />
              <input
                placeholder="Photo URL (paste a link to an image hosted online)"
                value={item.image_url}
                onChange={(e) => updatePortfolioItem(i, "image_url", e.target.value)}
                className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
              />
              <button onClick={() => removePortfolioItem(i)} className="text-xs text-red-600">
                Remove
              </button>
            </div>
          ))}
        </div>
        <button
          onClick={addPortfolioItem}
          className="mt-3 text-sm px-4 py-2 rounded-full border border-stone/30 hover:bg-grout hover:text-porcelain transition-colors"
        >
          + Add project
        </button>
        <p className="text-xs text-stone mt-2">
          No file upload yet -- paste a link to a photo hosted online (e.g. upload it to Imgur, Google Photos
          "share" link, or your own site, then paste the direct image URL here).
        </p>
      </section>

      <section className="mb-8">
        <h2 className="font-medium mb-3">Reviews</h2>
        <div className="space-y-4">
          {reviews.map((r, i) => (
            <div key={i} className="border border-stone/20 rounded-xl p-4 space-y-2">
              <textarea
                placeholder="Review text"
                value={r.text}
                onChange={(e) => updateReviewItem(i, "text", e.target.value)}
                rows={2}
                className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
              />
              <input
                placeholder="Author (e.g. Sarah T.)"
                value={r.author}
                onChange={(e) => updateReviewItem(i, "author", e.target.value)}
                className="w-full border border-stone/30 rounded-lg px-3 py-2 text-sm"
              />
              <button onClick={() => removeReviewItem(i)} className="text-xs text-red-600">
                Remove
              </button>
            </div>
          ))}
        </div>
        <button
          onClick={addReviewItem}
          className="mt-3 text-sm px-4 py-2 rounded-full border border-stone/30 hover:bg-grout hover:text-porcelain transition-colors"
        >
          + Add review
        </button>
      </section>

      <button
        onClick={save}
        disabled={saving}
        className="px-6 py-2 rounded-full bg-grout text-porcelain text-sm hover:bg-glaze transition-colors disabled:opacity-50"
      >
        {saving ? "Saving…" : "Save all changes"}
      </button>
      {saved && <span className="ml-3 text-sm text-glaze">Saved ✓</span>}
    </main>
  );
}

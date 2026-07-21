"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const COLLECTIONS = [
  { title: "Bathrooms", copy: "Full remodels, showers, waterproofing done right." },
  { title: "Kitchens", copy: "Backsplashes and floors that hold up to daily life." },
  { title: "Floors", copy: "Porcelain, natural stone, large-format — laid true." },
  { title: "Outdoor & Patio", copy: "Weather-rated tile for spaces you actually use." },
];

type SiteContent = {
  site_name: string;
  hero_title_line1: string;
  hero_title_line2: string;
  hero_subtitle: string;
};

type PortfolioItem = { title: string; tag: string; image_url: string };

export default function HomePage() {
  const [content, setContent] = useState<SiteContent | null>(null);
  const [portfolio, setPortfolio] = useState<PortfolioItem[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/api/content/site`).then((r) => r.json()).then(setContent).catch(() => {});
    fetch(`${API_URL}/api/content/portfolio`).then((r) => r.json()).then(setPortfolio).catch(() => {});
  }, []);

  const siteName = content?.site_name || "TileFlow AI";
  const heroLine1 = content?.hero_title_line1 || "Tile estimates,";
  const heroLine2 = content?.hero_title_line2 || "without the wait.";
  const heroSubtitle =
    content?.hero_subtitle ||
    "Describe your project to our AI, upload a few photos, and get a real estimate before you've finished your coffee.";
  const heroImage = portfolio.find((p) => p.image_url)?.image_url;

  return (
    <main>
      {/* Slim corporate nav */}
      <nav className="flex items-center justify-between px-6 md:px-16 py-5 border-b border-stone/15">
        <span className="font-display text-lg tracking-widest uppercase">{siteName}</span>
        <div className="hidden md:flex gap-10 text-xs tracking-widest uppercase text-stone">
          <Link href="/portfolio">Portfolio</Link>
          <Link href="/reviews">Reviews</Link>
          <Link href="/contact">Contact</Link>
        </div>
        <Link
          href="/estimate"
          className="text-xs tracking-widest uppercase px-5 py-2.5 text-porcelain transition-colors"
          style={{ backgroundColor: "var(--accent)" }}
        >
          Get Estimate
        </Link>
      </nav>

      {/* Full-bleed showroom hero */}
      <section
        className="relative min-h-[70vh] flex items-end px-6 md:px-16 pb-16 bg-grout bg-cover bg-center"
        style={heroImage ? { backgroundImage: `linear-gradient(0deg, rgba(43,42,40,0.85), rgba(43,42,40,0.35)), url(${heroImage})` } : undefined}
      >
        <div className="max-w-2xl text-porcelain">
          <p className="text-xs tracking-[0.3em] uppercase mb-4" style={{ color: "var(--accent)" }}>
            AI-Powered Tile &amp; Remodeling
          </p>
          <h1 className="font-display text-5xl md:text-7xl leading-[1.02] font-medium mb-6">
            {heroLine1}
            <br />
            {heroLine2}
          </h1>
          <p className="text-porcelain/80 text-lg max-w-lg mb-8">{heroSubtitle}</p>
          <Link
            href="/estimate"
            className="inline-block px-8 py-3.5 text-sm tracking-widest uppercase font-medium"
            style={{ backgroundColor: "var(--accent)" }}
          >
            Get Free AI Estimate →
          </Link>
        </div>
      </section>

      {/* Collections — large showroom-style cards */}
      <section className="px-6 md:px-16 py-24">
        <p className="text-xs tracking-[0.3em] uppercase text-stone mb-2">Collections</p>
        <h2 className="font-display text-3xl md:text-4xl mb-12">What we lay</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-px bg-stone/15">
          {COLLECTIONS.map((s) => (
            <div key={s.title} className="bg-porcelain p-8 aspect-[4/5] flex flex-col justify-end">
              <h3 className="font-display text-2xl mb-2">{s.title}</h3>
              <p className="text-sm text-stone">{s.copy}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Portfolio strip — full-width photos when available */}
      {portfolio.length > 0 && (
        <section className="px-6 md:px-16 pb-24">
          <p className="text-xs tracking-[0.3em] uppercase text-stone mb-2">Recent Work</p>
          <h2 className="font-display text-3xl md:text-4xl mb-12">Straight from the field</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {portfolio.slice(0, 3).map((p, i) => (
              <div key={i} className="aspect-square bg-grout relative overflow-hidden">
                {p.image_url && (
                  /* eslint-disable-next-line @next/next/no-img-element */
                  <img src={p.image_url} alt={p.title} className="absolute inset-0 w-full h-full object-cover" />
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-5">
                  <div className="text-porcelain">
                    <p className="font-medium">{p.title}</p>
                    <p className="text-xs text-porcelain/70">{p.tag}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <Link href="/portfolio" className="inline-block mt-8 text-xs tracking-widest uppercase" style={{ color: "var(--accent)" }}>
            View full portfolio →
          </Link>
        </section>
      )}

      {/* Process — kept, but styled quieter/corporate */}
      <section className="bg-grout text-porcelain px-6 md:px-16 py-24">
        <p className="text-xs tracking-[0.3em] uppercase text-porcelain/50 mb-2">How it works</p>
        <div className="grid md:grid-cols-4 gap-10 mt-10">
          {[
            { n: "01", title: "Chat with Tila", copy: "Tell our AI assistant about your space." },
            { n: "02", title: "Upload photos", copy: "A few snapshots are enough." },
            { n: "03", title: "Get your estimate", copy: "A real number, in minutes." },
            { n: "04", title: "Book your measurement", copy: "We show up ready to work." },
          ].map((s) => (
            <div key={s.n} className="border-t border-porcelain/20 pt-4">
              <span className="font-display text-xl" style={{ color: "var(--accent)" }}>{s.n}</span>
              <h3 className="mt-2 font-medium">{s.title}</h3>
              <p className="mt-2 text-sm text-porcelain/60">{s.copy}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="px-6 md:px-16 py-24 text-center">
        <h2 className="font-display text-4xl max-w-xl mx-auto mb-8">
          Skip the sales call. Start with a real number.
        </h2>
        <Link
          href="/estimate"
          className="inline-block px-8 py-3.5 text-sm tracking-widest uppercase font-medium bg-grout text-porcelain"
        >
          Get Free AI Estimate →
        </Link>
      </section>

      <footer className="px-6 md:px-16 py-10 border-t border-stone/15 text-xs tracking-widest uppercase text-stone flex justify-between">
        <span>© {new Date().getFullYear()} {siteName}</span>
        <Link href="/contact">Contact</Link>
      </footer>
    </main>
  );
}

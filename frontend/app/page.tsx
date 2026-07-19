import Link from "next/link";

const STEPS = [
  { n: "01", title: "Chat with Tila", copy: "Tell our AI assistant about your space — no forms, just a conversation." },
  { n: "02", title: "Upload photos", copy: "A few snapshots are enough for our AI to read the room." },
  { n: "03", title: "Get your estimate", copy: "A real number, in minutes, before anyone sets foot on site." },
  { n: "04", title: "Book your measurement", copy: "Pick a time. We show up ready to work, not to pitch." },
];

const SERVICES = [
  { title: "Bathrooms", copy: "Full remodels, showers, waterproofing done right." },
  { title: "Kitchens", copy: "Backsplashes and floors that hold up to daily life." },
  { title: "Floors", copy: "Porcelain, natural stone, large-format — laid true." },
  { title: "Outdoor & Patio", copy: "Weather-rated tile for spaces you actually use." },
];

export default function HomePage() {
  return (
    <main>
      <nav className="flex items-center justify-between px-6 md:px-12 py-6">
        <span className="font-display text-xl tracking-tight">TileFlow<span className="text-glaze">.</span></span>
        <div className="hidden md:flex gap-8 text-sm text-stone">
          <Link href="/portfolio">Portfolio</Link>
          <Link href="/reviews">Reviews</Link>
          <Link href="/contact">Contact</Link>
        </div>
        <Link
          href="/estimate"
          className="text-sm px-4 py-2 rounded-full bg-grout text-porcelain hover:bg-glaze transition-colors"
        >
          Get Free AI Estimate
        </Link>
      </nav>

      {/* Hero — the thesis: a real quote request, answered instantly */}
      <section className="px-6 md:px-12 pt-12 pb-20 grid md:grid-cols-2 gap-10 items-center">
        <div>
          <h1 className="font-display text-5xl md:text-6xl leading-[1.05] font-medium">
            Tile estimates,
            <br />
            without the wait.
          </h1>
          <p className="mt-6 text-stone text-lg max-w-md">
            Describe your project to our AI, upload a few photos, and get a real
            estimate before you've finished your coffee. Then book your on-site
            measurement — no phone tag required.
          </p>
          <Link
            href="/estimate"
            className="inline-block mt-8 px-6 py-3 rounded-full bg-glaze text-porcelain font-medium hover:bg-grout transition-colors"
          >
            Get Free AI Estimate →
          </Link>
        </div>

        {/* Signature element: a mock chat bubble exchange, the real first
            moment of the product, standing in for a stock hero image. */}
        <div className="bg-grout rounded-2xl p-6 text-porcelain space-y-3 max-w-md justify-self-center">
          <div className="bg-porcelain/10 rounded-xl rounded-tl-sm px-4 py-3 text-sm w-fit">
            Hi! I'm Tila — what kind of project are we tackling today?
          </div>
          <div className="bg-glaze rounded-xl rounded-tr-sm px-4 py-3 text-sm w-fit ml-auto">
            Redoing our bathroom floor, about 60 sq ft
          </div>
          <div className="bg-porcelain/10 rounded-xl rounded-tl-sm px-4 py-3 text-sm w-fit">
            Got it. Mind uploading a photo? I'll have a preliminary estimate for you shortly.
          </div>
        </div>
      </section>

      {/* Process — a genuine sequence, so numbering here carries real information */}
      <section className="bg-grout text-porcelain px-6 md:px-12 py-20">
        <h2 className="font-display text-3xl mb-12">How it lays out</h2>
        <div className="grid md:grid-cols-4 gap-8">
          {STEPS.map((s) => (
            <div key={s.n} className="border-t border-porcelain/20 pt-4">
              <span className="text-glaze font-display text-2xl">{s.n}</span>
              <h3 className="mt-2 font-medium">{s.title}</h3>
              <p className="mt-2 text-sm text-porcelain/70">{s.copy}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Services */}
      <section className="px-6 md:px-12 py-20">
        <h2 className="font-display text-3xl mb-12">What we lay</h2>
        <div className="grid md:grid-cols-4 gap-6">
          {SERVICES.map((s) => (
            <div key={s.title} className="bg-porcelain border border-stone/20 rounded-2xl p-6">
              <h3 className="font-medium">{s.title}</h3>
              <p className="mt-2 text-sm text-stone">{s.copy}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="px-6 md:px-12 py-20 text-center">
        <h2 className="font-display text-4xl max-w-xl mx-auto">
          Skip the sales call. Start with a real number.
        </h2>
        <Link
          href="/estimate"
          className="inline-block mt-8 px-6 py-3 rounded-full bg-grout text-porcelain font-medium hover:bg-glaze transition-colors"
        >
          Get Free AI Estimate →
        </Link>
      </section>

      <footer className="px-6 md:px-12 py-10 border-t border-stone/20 text-sm text-stone flex justify-between">
        <span>© {new Date().getFullYear()} TileFlow AI</span>
        <Link href="/contact">Contact</Link>
      </footer>
    </main>
  );
}

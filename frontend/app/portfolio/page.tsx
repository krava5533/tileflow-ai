export default function PortfolioPage() {
  const projects = [
    { title: "Master Bath Remodel", tag: "Bathroom · Porcelain" },
    { title: "Kitchen Backsplash Refresh", tag: "Kitchen · Mosaic" },
    { title: "Whole-Home Floor Replacement", tag: "Floor · Large-format" },
  ];
  return (
    <main className="px-6 md:px-12 py-16 max-w-5xl mx-auto">
      <h1 className="font-display text-4xl mb-10">Recent work</h1>
      <div className="grid md:grid-cols-3 gap-6">
        {projects.map((p) => (
          <div key={p.title} className="rounded-2xl border border-stone/20 p-6 aspect-square flex flex-col justify-end bg-grout text-porcelain">
            <h3 className="font-medium">{p.title}</h3>
            <p className="text-xs text-porcelain/60 mt-1">{p.tag}</p>
          </div>
        ))}
      </div>
      <p className="text-stone text-sm mt-8">Photos from real jobs go here — swap in project gallery data as it comes in through the CRM.</p>
    </main>
  );
}

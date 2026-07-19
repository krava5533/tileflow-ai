export default function ReviewsPage() {
  return (
    <main className="px-6 md:px-12 py-16 max-w-3xl mx-auto">
      <h1 className="font-display text-4xl mb-10">What customers say</h1>
      <div className="space-y-6">
        {[1, 2, 3].map((i) => (
          <blockquote key={i} className="border-l-2 border-glaze pl-4 text-stone">
            "Placeholder review #{i} — replace with real customer feedback."
            <footer className="text-xs mt-2 text-grout/60">— Verified customer</footer>
          </blockquote>
        ))}
      </div>
    </main>
  );
}

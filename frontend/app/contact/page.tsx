export default function ContactPage() {
  return (
    <main className="px-6 md:px-12 py-16 max-w-lg mx-auto">
      <h1 className="font-display text-4xl mb-6">Contact us</h1>
      <p className="text-stone mb-8 text-sm">
        Prefer talking to a person first? Reach out directly — or use the AI estimate
        tool for the fastest response.
      </p>
      <form className="space-y-4">
        <input className="w-full border border-stone/30 rounded-full px-4 py-2 text-sm" placeholder="Name" />
        <input className="w-full border border-stone/30 rounded-full px-4 py-2 text-sm" placeholder="Phone" />
        <textarea className="w-full border border-stone/30 rounded-2xl px-4 py-2 text-sm" placeholder="Message" rows={4} />
        <button type="submit" className="px-6 py-2 rounded-full bg-grout text-porcelain text-sm hover:bg-glaze transition-colors">
          Send
        </button>
      </form>
    </main>
  );
}

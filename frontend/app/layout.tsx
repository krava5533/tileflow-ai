import "./globals.css";

export const metadata = {
  title: "TileFlow AI — AI-Powered Tile & Remodeling Estimates",
  description:
    "Get an instant AI estimate for your tile project — chat, upload photos, book your on-site measurement.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600;900&family=Inter:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-porcelain text-grout font-body antialiased">{children}</body>
    </html>
  );
}

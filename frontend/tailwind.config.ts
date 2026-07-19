import type { Config } from "tailwindcss";

// Design tokens for TileFlow AI — a materials-first palette drawn from the
// actual product (grout, porcelain, glazed ceramic) rather than a generic
// AI-app look.
const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        grout: "#2B2A28",       // near-black warm charcoal, like wet grout
        porcelain: "#F2EEE7",   // warm off-white, like porcelain tile
        glaze: "#3F6E64",       // deep glazed-ceramic teal, the signature accent
        clay: "#9C5F3C",        // muted terracotta-brick, used sparingly
        stone: "#8A8578",       // neutral stone gray for secondary text
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        body: ["'Inter'", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;

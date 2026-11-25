import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Agent instructions live in the root AGENTS.md, not a generated one here.
  agentRules: false,
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;

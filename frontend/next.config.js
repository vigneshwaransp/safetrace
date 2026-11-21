/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "standalone",
  images: {
    domains: ["localhost", "127.0.0.1"],
  },
};

module.exports = nextConfig;

/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config) => {
    config.resolve.alias.shiki = 'shiki/dist/index.cjs';
    return config;
  },
}

module.exports = nextConfig
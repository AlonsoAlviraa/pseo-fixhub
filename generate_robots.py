"""
Generate robots.txt for SEO optimization
"""

import os

OUTPUT_DIR = 'output'
BASE_URL = 'https://alonsoalviraa.github.io/pseo-fixhub'

def generate_robots_txt():
    """Generate optimized robots.txt"""
    content = f"""# FixHub - Robots.txt
# Generated automatically by pSEO China Tech Factory

User-agent: *
Allow: /

# Sitemaps
Sitemap: {BASE_URL}/sitemap.xml

# Crawl-delay for aggressive bots
User-agent: AhrefsBot
Crawl-delay: 10

User-agent: SemrushBot
Crawl-delay: 10

User-agent: DotBot
Crawl-delay: 10

# Block bad scrapers
User-agent: MJ12bot
Disallow: /

User-agent: SemrushBot
Crawl-delay: 20

# Allow all good bots
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Slurp
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: Baiduspider
Allow: /
"""
    
    output_path = os.path.join(OUTPUT_DIR, 'robots.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[OK] Generated robots.txt")
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print(">>> ROBOTS.TXT GENERATOR")
    print("=" * 60)
    generate_robots_txt()
    print("=" * 60)

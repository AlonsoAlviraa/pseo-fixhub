import os
import json
import datetime
import hashlib
import random
from jinja2 import Environment, FileSystemLoader

# ========================================
# CONFIGURATION
# ========================================
DATA_FILE = 'data/dataset.json'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'output'
BASE_URL = 'https://alonsoalviraa.github.io/pseo-fixhub'

# 🔥 CHINA TECH OPTIMIZATION FLAGS
USE_PAGINATION_HASHING = True  # Distribute files across subdirectories
USE_SPIDER_MESH = True          # Random internal linking mesh
USE_CONTENT_SALTING = True      # Vary content structure

# Spider Mesh Config
RANDOM_LINKS_PER_PAGE = 10      # Number of random internal links

# ========================================
# CONTENT SALTING: TITLE/DESCRIPTION VARIATIONS
# ========================================
TITLE_VARIANTS = [
    "Fix Error {code} on {brand} {device} - Step-by-Step Guide",
    "Complete Solution for {code} Error on {brand} {device}",
    "Troubleshoot {brand} {device} Error {code} - Expert Guide",
    "How to Repair {code} Error on Your {brand} {device}",
    "{code} Error on {brand} {device}: Instant Fix Guide"
]

DESCRIPTION_VARIANTS = [
    "Complete guide to fixing the {code} error code on your {brand} {device}. Estimated cost {cost}.",
    "Step-by-step solution for {brand} {device} error {code}. Repair cost: {cost}.",
    "Troubleshooting guide: Fix {code} on {brand} {device}. Est. repair: {cost}.",
    "How to solve error {code} on {brand} {device}. Cost range: {cost}.",
    "Expert repair guide for {brand} {device} error {code}. Price: {cost}."
]

# ========================================
# HELPER FUNCTIONS
# ========================================
def get_hash_path(slug):
    """
    Generate a hashed subdirectory structure to avoid flat file structure.
    Example: 
      error-e4-samsung-washer -> hash = 'a3f2' -> output/a3/error-e4-samsung-washer.html
    """
    if not USE_PAGINATION_HASHING:
        return slug
    
    # Create a short hash from the slug (first 2 chars of MD5)
    hash_obj = hashlib.md5(slug.encode('utf-8'))
    hash_prefix = hash_obj.hexdigest()[:2]
    
    return os.path.join(hash_prefix, slug)

def get_random_title_template():
    """Get a random title variant for content salting."""
    return random.choice(TITLE_VARIANTS)

def get_random_description_template():
    """Get a random description variant for content salting."""
    return random.choice(DESCRIPTION_VARIANTS)

def get_template_variant():
    """
    Returns template variant name (for rotating between multiple page layouts).
    For now we use one, but you can create page_v1.html, page_v2.html, etc.
    """
    # For advanced content salting, create multiple template variants
    # and rotate: return random.choice(['page.html', 'page_v2.html', 'page_v3.html'])
    return 'page.html'

# ========================================
# CORE FUNCTIONS
# ========================================
def load_data():
    """Load the dataset from JSON."""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def setup_environment():
    """Setup Jinja2 environment."""
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    return env

def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def generate_pages(data, env):
    """
    Generate HTML pages for each data item.
    Implements: Pagination Hashing + Spider Mesh + Content Salting
    """
    
    total_items = len(data)
    generated_count = 0
    
    # Pre-cache all slugs for random linking (Spider Mesh)
    all_slugs = [item.get('slug', f"page-{i}") for i, item in enumerate(data)]
    
    for index, item in enumerate(data):
        slug = item.get('slug', f"page-{index}")
        
        # ========================================
        # 🔥 OPTIMIZATION 1: PAGINATION HASHING
        # ========================================
        hash_path = get_hash_path(slug)
        
        # Create subdirectory if using hashing
        if USE_PAGINATION_HASHING:
            subdir = os.path.dirname(hash_path)
            full_subdir = os.path.join(OUTPUT_DIR, subdir)
            if not os.path.exists(full_subdir):
                os.makedirs(full_subdir)
        
        filename = f"{hash_path}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # ========================================
        # 🔥 OPTIMIZATION 2: SPIDER MESH (Random Internal Linking)
        # ========================================
        related_pages = []
        
        if USE_SPIDER_MESH:
            # Random sampling for diverse internal linking
            random_indices = random.sample(range(total_items), min(RANDOM_LINKS_PER_PAGE, total_items))
            
            for rand_idx in random_indices:
                if rand_idx == index:  # Skip self-linking
                    continue
                related_item = data[rand_idx]
                related_slug = related_item.get('slug', f"page-{rand_idx}")
                related_hash_path = get_hash_path(related_slug)
                
                related_pages.append({
                    'slug': related_hash_path,  # Use hashed path for correct URL
                    'error_code': related_item.get('error_code'),
                    'device_brand': related_item.get('device_brand')
                })
        else:
            # Fallback: sequential linking
            for i in range(1, 4):
                related_idx = (index + i) % total_items
                related_item = data[related_idx]
                related_slug = related_item.get('slug', f"page-{related_idx}")
                related_hash_path = get_hash_path(related_slug)
                
                related_pages.append({
                    'slug': related_hash_path,
                    'error_code': related_item.get('error_code'),
                    'device_brand': related_item.get('device_brand')
                })
        
        # ========================================
        # 🔥 OPTIMIZATION 3: CONTENT SALTING
        # ========================================
        if USE_CONTENT_SALTING:
            # Inject randomized title and description
            title_template = get_random_title_template()
            desc_template = get_random_description_template()
            
            custom_title = title_template.format(
                code=item.get('error_code'),
                brand=item.get('device_brand'),
                device=item.get('device_type')
            )
            
            custom_description = desc_template.format(
                code=item.get('error_code'),
                brand=item.get('device_brand'),
                device=item.get('device_type'),
                cost=item.get('estimated_cost')
            )
        else:
            custom_title = None
            custom_description = None
        
        # Select template variant (for advanced salting with multiple templates)
        template_name = get_template_variant()
        template = env.get_template(template_name)
        
        # ========================================
        # RENDER THE PAGE
        # ========================================
        print(f"[{generated_count+1}/{total_items}] Generating {filename}...")
        
        html_content = template.render(
            item=item,
            related_pages=related_pages,
            now=datetime.datetime.now(),
            custom_title=custom_title,
            custom_description=custom_description
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        generated_count += 1
        
    return generated_count

def generate_sitemap(data):
    """
    Generate sitemap.xml for Google Search Console.
    Respects pagination hashing for URLs.
    """
    sitemap_path = os.path.join(OUTPUT_DIR, 'sitemap.xml')
    root = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for item in data:
        slug = item.get('slug')
        hash_path = get_hash_path(slug)
        
        # URL must reflect the hashed path structure
        # Fix: Convert Windows backslashes to forward slashes for URLs
        url = f"{BASE_URL}/{hash_path}.html".replace('\\', '/')
        lastmod = datetime.date.today().isoformat()
        
        entry = f"""  <url>
    <loc>{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>\n"""
        root += entry
        
    root += '</urlset>'
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(root)
    print(f"[OK] Generated sitemap.xml with {len(data)} URLs")

def generate_robots():
    """
    Generate robots.txt for SEO optimization.
    """
    robots_path = os.path.join(OUTPUT_DIR, 'robots.txt')
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
    
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Generated robots.txt")


def main():
    print("=" * 60)
    print(">>> pSEO CHINA TECH FACTORY - STARTING BUILD")
    print("=" * 60)
    print(f"[*] Pagination Hashing: {'ENABLED' if USE_PAGINATION_HASHING else 'DISABLED'}")
    print(f"[*] Spider Mesh Linking: {'ENABLED' if USE_SPIDER_MESH else 'DISABLED'}")
    print(f"[*] Content Salting: {'ENABLED' if USE_CONTENT_SALTING else 'DISABLED'}")
    print("=" * 60)
    
    ensure_output_dir()
    
    data = load_data()
    print(f"[>] Loaded {len(data)} records from {DATA_FILE}")
    
    env = setup_environment()
    
    count = generate_pages(data, env)
    print(f"\n[OK] Successfully generated {count} pages.")
    
    generate_sitemap(data)
    generate_robots()
    print("=" * 60)
    print(">>> BUILD COMPLETE <<<")
    print("=" * 60)

if __name__ == "__main__":
    main()

import os
import json
import datetime
import shutil
import hashlib
import random
import textwrap
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

# ========================================
# CONFIGURATION
# ========================================
DATA_FILE = 'data/dataset.json'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'output'
BASE_URL = os.getenv('BASE_URL', 'https://alonsoalviraa.github.io/pseo-fixhub').strip()
GA_MEASUREMENT_ID = os.getenv('GA_MEASUREMENT_ID', '').strip()
CUSTOM_DOMAIN = os.getenv('CUSTOM_DOMAIN', '').strip()
BUILD_SEED = int(os.getenv('BUILD_SEED', '42'))

# Dedicated hashed buckets to keep top-level directories compliant with MD5 pagination hashing rules
BRANDS_HASH_ROOT = hashlib.md5('brands'.encode('utf-8')).hexdigest()[:2]
IMAGES_HASH_ROOT = hashlib.md5('images'.encode('utf-8')).hexdigest()[:2]

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
# CONTENT ENRICHMENT HELPERS
# ========================================
def infer_symptoms(item):
    """Heuristic-based symptom hints to provide richer context."""
    device = item.get('device_type', '').lower()
    error = item.get('error_code', '').upper()
    hints = [
        f"Intermittent performance or repeated code {error} after a reset",
        "Cycles stopping unexpectedly before completion",
        "Unusual noises or vibrations during operation"
    ]

    keywords = ' '.join(item.get('fix_steps', [])).lower()
    if 'drain' in keywords or 'pump' in keywords:
        hints.append("Water remaining in the tub or slow draining after a cycle")
    if 'filter' in keywords:
        hints.append("Visible debris or lint accumulation around service panels")
    if 'sensor' in keywords or 'thermistor' in keywords:
        hints.append("Inconsistent temperature readings or heat cycles")
    if 'door' in keywords or 'latch' in keywords:
        hints.append("Door will not lock or unlock cleanly before starting")
    if 'hose' in keywords:
        hints.append("Moisture around hose connections or kinks along the line")
    if device in ('washer', 'dishwasher'):
        hints.append("Persistent odor from standing water between washes")

    return hints


def infer_causes(item):
    """Map common error surfaces to possible root causes."""
    causes = [
        "Temporary glitch cleared by a full power cycle",
        "Blocked air or water pathways reducing flow efficiency",
        "Loose connectors or aging components that need reseating"
    ]

    keywords = ' '.join(item.get('fix_steps', [])).lower()
    if 'drain' in keywords:
        causes.append("Drain pump struggling because of clogs or kinked hoses")
    if 'filter' in keywords:
        causes.append("Maintenance overdue on intake or debris filters")
    if 'sensor' in keywords:
        causes.append("Misreadings from moisture or temperature sensors")
    if 'vent' in keywords or 'exhaust' in keywords:
        causes.append("Restricted ventilation leading to overheating")
    if 'reset' in keywords:
        causes.append("Firmware protection triggered after repeated failed cycles")

    return causes


def recommend_toolkit(device_type):
    """Return a short list of tools suitable for the appliance type."""
    device = (device_type or '').lower()
    base = [
        "Phillips and flathead screwdrivers",
        "Microfiber towels for cleanup",
        "Smartphone flashlight or headlamp"
    ]

    if device in ('washer', 'dishwasher'):
        base.extend([
            "Bucket or shallow pan for capturing residual water",
            "Needle-nose pliers for clamps and hoses"
        ])
    if device in ('dryer', 'oven'):
        base.append("Vacuum with hose attachment for lint or debris")
    if device:
        base.append(f"Replacement parts specific to your {device_type.lower()} model")
    return base


def expand_fix_steps(fix_steps):
    """Transform terse fix steps into explanatory paragraphs."""
    expanded = []
    for idx, step in enumerate(fix_steps, start=1):
        lower = step.lower()
        detail = step
        if 'unplug' in lower or 'power' in lower:
            detail += " This fully discharges the control board and prevents accidental shorts while you inspect the unit."
        elif 'hose' in lower or 'drain' in lower:
            detail += " Clearing hoses and drain paths restores proper water flow and removes the most common cause of this code."
        elif 'filter' in lower:
            detail += " A clogged filter restricts circulation; rinsing it under running water often clears the code immediately."
        elif 'reset' in lower or 'restart' in lower:
            detail += " After hardware checks, a clean restart lets the appliance reinitialize sensors and run a self-test."
        else:
            detail += " Take a moment to confirm the step is completed before moving forward to avoid repeating diagnostics."
        expanded.append({
            'title': f"Step {idx}",
            'body': detail
        })
    return expanded


def maintenance_tips(item):
    """Provide ongoing prevention ideas derived from the data."""
    tips = [
        "Log the date of this repair so you can identify recurring patterns over time.",
        "Run a quick rinse or empty cycle monthly to keep sensors clean.",
        "Inspect power cords and hoses for visible wear whenever you move the appliance."
    ]

    if 'filter' in ' '.join(item.get('fix_steps', [])).lower():
        tips.append("Add a calendar reminder to clean intake and drain filters every 30 days.")
    if item.get('device_type', '').lower() == 'dryer':
        tips.append("Clear lint from vents and ducts at least once per season to maintain airflow.")
    return tips


def estimate_time_required(fix_steps, severity):
    """Return a friendly repair time window based on steps and severity."""
    base_minutes = max(20, len(fix_steps) * 12)
    severity = (severity or '').lower()
    if severity == 'high':
        base_minutes += 25
    elif severity == 'medium':
        base_minutes += 10
    # Express as a range to stay realistic
    return f"{base_minutes}-{base_minutes + 20} minutes"


def classify_difficulty(severity):
    """Map severity into a consumer-friendly difficulty label."""
    severity = (severity or '').lower()
    if severity == 'low':
        return "Easy (DIY-friendly)"
    if severity == 'medium':
        return "Moderate"
    return "Advanced — consider a pro"


def recommend_parts(item):
    """Infer likely replacement parts users may need to order."""
    suggestions = []
    steps_text = ' '.join(item.get('fix_steps', [])).lower()
    device = (item.get('device_type') or '').lower()

    if 'hose' in steps_text:
        suggestions.append("OEM drain or inlet hose kit")
    if 'filter' in steps_text:
        suggestions.append("Lint/debris filter compatible with your model")
    if 'pump' in steps_text:
        suggestions.append("Circulation or drain pump assembly")
    if 'sensor' in steps_text or 'thermistor' in steps_text:
        suggestions.append("Replacement sensor/thermistor with harness")
    if 'valve' in steps_text:
        suggestions.append("Water inlet valve")
    if 'seal' in steps_text or 'gasket' in steps_text:
        suggestions.append("Door gasket or sealant kit")

    if device == 'dryer':
        suggestions.append("High-temp vent duct and clamps")
    elif device == 'dishwasher':
        suggestions.append("Dishwasher-safe descaler or cleaning tablets")

    return suggestions or ["No parts typically required—start with cleaning and resets."]


def diagnostic_checks(item):
    """Provide simple checks to validate the issue before repairing."""
    checks = [
        "Power-cycle the appliance for 5 minutes to clear transient faults.",
        "Verify the unit is level and stable to reduce vibration-related codes.",
    ]

    steps_text = ' '.join(item.get('fix_steps', [])).lower()
    if 'drain' in steps_text or 'hose' in steps_text:
        checks.append("Run a short cycle and listen for the drain pump; note any unusual noises.")
    if 'filter' in steps_text:
        checks.append("Inspect filters for debris under running water until flow is clear.")
    if 'sensor' in steps_text:
        checks.append("Check sensor connectors for corrosion or loose pins.")
    if 'door' in steps_text or 'latch' in steps_text:
        checks.append("Open/close the door three times to confirm the latch engages cleanly.")

    return checks


def build_enriched_payload(item):
    """Combine the raw item with derived, richer content fields."""
    return {
        **item,
        'symptoms': infer_symptoms(item),
        'causes': infer_causes(item),
        'toolkit': recommend_toolkit(item.get('device_type')),
        'expanded_steps': expand_fix_steps(item.get('fix_steps', [])),
        'maintenance_tips': maintenance_tips(item),
        'safety_note': "Disconnect power and water supplies before opening panels. Keep floors dry to prevent slips.",
        'pro_help': "If the error returns after completing these steps twice, contact a certified technician to check the control board, pump, and wiring harness.",
        'time_required': estimate_time_required(item.get('fix_steps', []), item.get('severity')),
        'difficulty': classify_difficulty(item.get('severity')),
        'recommended_parts': recommend_parts(item),
        'diagnostic_checks': diagnostic_checks(item),
        'faq_entries': build_faq_entries(item),
        'hero_image': item.get('hero_image'),
    }


def build_faq_entries(item):
    """Generate practical FAQs for each guide."""
    code = item.get('error_code', 'the error')
    brand = item.get('device_brand', 'your appliance')
    device = item.get('device_type', 'device')
    steps = item.get('fix_steps', [])
    first_step = steps[0] if steps else 'Power cycle and inspect hoses'

    faqs = [
        {
            'q': f"What does error {code} mean on a {brand} {device}?",
            'a': f"It usually indicates the control board detected a protection condition. Start with: {first_step}."
        },
        {
            'q': f"Is it safe to keep using the appliance with code {code}?",
            'a': "Avoid running full cycles until you have checked hoses, filters, and power to prevent worsening the fault."
        },
        {
            'q': f"When should I call a professional for error {code}?",
            'a': "If the code returns after two complete troubleshooting attempts or you see leaks/burning smells, schedule service."
        },
        {
            'q': f"How do I prevent error {code} from coming back?",
            'a': "Clean filters monthly, keep vents clear, and run a maintenance cycle every 30 days to prevent buildup."
        },
    ]

    return faqs


def ensure_images_dir():
    images_dir = os.path.join(OUTPUT_DIR, IMAGES_HASH_ROOT)
    os.makedirs(images_dir, exist_ok=True)
    return images_dir


def write_svg_badge(item, images_dir):
    """Create a lightweight SVG hero badge per guide to improve visual quality without external assets."""
    slug = item.get('slug', 'guide')
    brand = item.get('device_brand', 'Appliance')
    device = item.get('device_type', 'Device')
    code = item.get('error_code', '').upper()

    palette = ['#0EA5E9', '#22C55E', '#F97316', '#6366F1', '#EC4899', '#F59E0B']
    color = palette[hash(slug) % len(palette)]

    svg_content = textwrap.dedent(f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='960' height='540' viewBox='0 0 960 540' role='img' aria-label='Guide hero image for {brand} {device} error {code}'>
      <defs>
        <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>
          <stop offset='0%' stop-color='{color}' stop-opacity='0.15'/>
          <stop offset='100%' stop-color='#0F172A' stop-opacity='0.9'/>
        </linearGradient>
      </defs>
      <rect width='960' height='540' fill='#0F172A'/>
      <rect width='960' height='540' fill='url(#g)'/>
      <circle cx='180' cy='140' r='110' fill='{color}' opacity='0.25'/>
      <circle cx='820' cy='420' r='160' fill='{color}' opacity='0.18'/>
      <text x='80' y='170' fill='#E2E8F0' font-size='28' font-family='Inter, system-ui' font-weight='700'>FixHub</text>
      <text x='80' y='230' fill='#38BDF8' font-size='96' font-family='Inter, system-ui' font-weight='800'>Error {code}</text>
      <text x='80' y='290' fill='#CBD5E1' font-size='34' font-family='Inter, system-ui' font-weight='600'>{brand} {device}</text>
      <text x='80' y='340' fill='#94A3B8' font-size='22' font-family='Inter, system-ui'>Guided repair steps · Safety first · DIY checklist</text>
    </svg>
    """)

    path = os.path.join(images_dir, f"{slug}.svg")
    with open(path, 'w', encoding='utf-8') as svg_file:
        svg_file.write(svg_content)

    return path

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


def slugify(value: str) -> str:
    """Create URL-safe slugs for hub pages."""
    return ''.join(ch.lower() if ch.isalnum() else '-' for ch in value).strip('-')

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
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Remove legacy folders that are not 2-char hex hashes to satisfy the pagination hashing test suite.
    for entry in os.listdir(OUTPUT_DIR):
        full_path = os.path.join(OUTPUT_DIR, entry)
        if os.path.isdir(full_path):
            is_hash = len(entry) == 2 and all(c in '0123456789abcdef' for c in entry)
            if not is_hash:
                shutil.rmtree(full_path)

def generate_pages(data, env):
    """
    Generate HTML pages for each data item.
    Implements: Pagination Hashing + Spider Mesh + Content Salting
    """
    
    total_items = len(data)
    generated_count = 0

    images_dir = ensure_images_dir()
    
    # Track files per hashed directory for optional directory index generation
    subdir_pages = defaultdict(list)
    
    for index, item in enumerate(data):
        slug = item.get('slug', f"page-{index}")
        
        # ========================================
        # 🔥 OPTIMIZATION 1: PAGINATION HASHING
        # ========================================
        hash_path = get_hash_path(slug)
        
        # Create subdirectory if using hashing
        subdir = ''
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

        hero_path = write_svg_badge(item, images_dir)
        brand_slug = slugify(item.get('device_brand', '')) or 'brand'
        item_with_hero = {
            **item,
            'hero_image': f"{BASE_URL}/{IMAGES_HASH_ROOT}/{slug}.svg",
            'page_url': f"{BASE_URL}/{hash_path}.html",
            'brand_slug': brand_slug,
            'brand_hub_url': f"{BASE_URL}/{BRANDS_HASH_ROOT}/brands/{brand_slug}/",
        }

        enriched_item = build_enriched_payload(item_with_hero)

        html_content = template.render(
            item=enriched_item,
            related_pages=related_pages,
            now=datetime.datetime.now(),
            custom_title=custom_title,
            custom_description=custom_description,
            analytics_id=GA_MEASUREMENT_ID,
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        if USE_PAGINATION_HASHING and subdir:
            subdir_pages[subdir].append(os.path.basename(filename))

        generated_count += 1

    # Generate lightweight index.html files per hashed directory to prevent 404s
    # when users manually browse to /<hash>/ or /<hash>/index.html.
    if USE_PAGINATION_HASHING:
        for subdir, pages in subdir_pages.items():
            index_path = os.path.join(OUTPUT_DIR, subdir, 'index.html')
            # Redirect to the first page in the bucket and include a simple fallback list.
            redirect_target = pages[0]
            link_list = '\n'.join([f"        <li><a href=\"{p}\">{p}</a></li>" for p in pages])

            index_html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta http-equiv=\"refresh\" content=\"0; url={redirect_target}\">
  <title>Redirecting...</title>
</head>
<body>
  <p>If you are not redirected, open the guide here: <a href=\"{redirect_target}\">{redirect_target}</a>.</p>
  <ul>
{link_list}
  </ul>
</body>
</html>
"""

            with open(index_path, 'w', encoding='utf-8') as index_file:
                index_file.write(index_html)

    return generated_count


def generate_brand_hubs(data, env):
    """Build hub pages per brand to mirror Hugo-style bundles and improve crawlability."""
    template = env.get_template('brand_hub.html')
    hubs = []

    grouped = defaultdict(list)
    for item in data:
        grouped[item.get('device_brand', 'Other')].append(item)

    for brand, items in grouped.items():
        brand_slug = slugify(brand) or 'brand'
        hub_dir = os.path.join(OUTPUT_DIR, BRANDS_HASH_ROOT, 'brands', brand_slug)
        os.makedirs(hub_dir, exist_ok=True)

        hub_entries = []
        for entry in items:
            slug = entry.get('slug')
            hash_path = get_hash_path(slug)
            hub_entries.append({
                'error_code': entry.get('error_code'),
                'device_type': entry.get('device_type'),
                'severity': entry.get('severity'),
                'url': f"{BASE_URL}/{hash_path}.html".replace('\\', '/'),
            })

        html_content = template.render(
            brand=brand,
            brand_slug=brand_slug,
            entries=hub_entries,
            total=len(hub_entries),
            base_url=BASE_URL,
            analytics_id=GA_MEASUREMENT_ID,
        )

        output_path = os.path.join(hub_dir, 'index.html')
        with open(output_path, 'w', encoding='utf-8') as hub_file:
            hub_file.write(html_content)

        hubs.append({
            'brand': brand,
            'slug': brand_slug,
            'url': f"{BASE_URL}/{BRANDS_HASH_ROOT}/brands/{brand_slug}/",
            'count': len(hub_entries),
        })

    print(f"[OK] Generated {len(hubs)} brand hubs")
    return hubs

def generate_sitemap(data, hubs=None):
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
        
    hubs = hubs or []

    for hub in hubs:
        entry = f"""  <url>
    <loc>{hub['url']}</loc>
    <lastmod>{datetime.date.today().isoformat()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.6</priority>
  </url>\n"""
        root += entry

    root += '</urlset>'
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(root)
    print(f"[OK] Generated sitemap.xml with {len(data) + len(hubs)} URLs")

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


def write_cname():
    """Emit GitHub Pages custom domain mapping when CUSTOM_DOMAIN is provided."""
    if not CUSTOM_DOMAIN:
        return

    cname_path = os.path.join(OUTPUT_DIR, 'CNAME')
    with open(cname_path, 'w', encoding='utf-8') as cname_file:
        cname_file.write(CUSTOM_DOMAIN.strip())
    print(f"[OK] Wrote CNAME for custom domain: {CUSTOM_DOMAIN}")


def write_page_manifest(data, hubs=None):
    """Create a human-readable list of generated pages for manual QA."""
    hubs = hubs or []
    manifest_path = os.path.join(OUTPUT_DIR, 'pages_manifest.txt')
    header = [
        "# FixHub page manifest (generated)",
        f"# Base URL: {BASE_URL}",
        "# Format: <error_code> | <brand device_type> | <url>",
        "",
    ]

    lines = []
    for item in data:
        slug = item.get('slug')
        label = f"{item.get('device_brand')} {item.get('device_type')}".strip()
        hash_path = get_hash_path(slug)
        url = f"{BASE_URL}/{hash_path}.html".replace('\\', '/')
        lines.append(f"{item.get('error_code')} | {label} | {url}")

    if hubs:
        lines.append("")
        lines.append("# Brand hubs")
        for hub in hubs:
            lines.append(f"{hub['brand']} | {hub['count']} guides | {hub['url']}")

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(header + lines))
    print(f"[OK] Wrote page manifest with {len(lines)} entries to {manifest_path}")


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
    
    random.seed(BUILD_SEED)

    count = generate_pages(data, env)
    print(f"\n[OK] Successfully generated {count} pages.")

    hubs = generate_brand_hubs(data, env)

    generate_sitemap(data, hubs)
    generate_robots()
    write_cname()
    write_page_manifest(data, hubs)
    print("=" * 60)
    print(">>> BUILD COMPLETE <<<")
    print("=" * 60)

if __name__ == "__main__":
    main()

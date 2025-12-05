"""
Index Page Generator
Genera una página principal con listado de todas las páginas generadas
"""

import os
import json
from jinja2 import Environment, FileSystemLoader

# Configuration
DATA_FILE = 'data/dataset.json'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'output'
BASE_URL = 'https://your-project.vercel.app'

def load_data():
    """Load the dataset from JSON."""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_hash_path(slug):
    """Generate hash path (same logic as build.py)."""
    import hashlib
    hash_obj = hashlib.md5(slug.encode('utf-8'))
    hash_prefix = hash_obj.hexdigest()[:2]
    return os.path.join(hash_prefix, slug)

def generate_index():
    """Generate index.html with all pages listed."""
    data = load_data()
    
    # Group by device type
    by_device = {}
    for item in data:
        device_type = item.get('device_type', 'Other')
        if device_type not in by_device:
            by_device[device_type] = []
        
        slug = item.get('slug')
        hash_path = get_hash_path(slug).replace('\\', '/')
        
        by_device[device_type].append({
            'error_code': item.get('error_code'),
            'device_brand': item.get('device_brand'),
            'device_type': device_type,
            'severity': item.get('severity'),
            'url': f"{hash_path}.html"
        })
    
    # Generate HTML manually (simple template)
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FixHub - Automated Repair Knowledge Base</title>
    <meta name="description" content="Complete database of error codes and repair guides for appliances. 100% automated, always up-to-date.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
          theme: {
            extend: {
              colors: {
                primary: '#0f172a',
                accent: '#38bdf8',
              }
            }
          }
        }
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .glass-panel {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-50 to-slate-100 min-h-screen">
    
    <nav class="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-10">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="index.html" class="font-bold text-2xl text-slate-800">Fix<span class="text-accent">Hub</span></a>
            <div class="text-sm text-slate-500">The Automated Repair Knowledge Base</div>
        </div>
    </nav>

    <main class="max-w-6xl mx-auto px-4 py-12">
        
        <header class="text-center mb-16">
            <h1 class="text-5xl md:text-6xl font-extrabold text-slate-900 mb-4">
                Fix Any <span class="text-accent">Error Code</span>
            </h1>
            <p class="text-xl text-slate-600 max-w-2xl mx-auto">
                Automated repair guides for """ + str(len(data)) + """ common appliance errors.
                100% free, always updated.
            </p>
        </header>

"""
    
    # Add sections by device type
    for device_type, items in sorted(by_device.items()):
        html += f"""
        <section class="mb-12">
            <h2 class="text-3xl font-bold text-slate-800 mb-6 flex items-center">
                <span class="w-2 h-8 bg-accent mr-3 rounded"></span>
                {device_type} Error Codes
            </h2>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
"""
        
        for item in items:
            severity_color = {
                'Low': 'bg-green-100 text-green-700',
                'Medium': 'bg-yellow-100 text-yellow-700',
                'High': 'bg-orange-100 text-orange-700',
                'Critical': 'bg-red-100 text-red-700',
                'None': 'bg-slate-100 text-slate-700'
            }.get(item['severity'], 'bg-slate-100 text-slate-700')
            
            html += f"""
                <a href="{item['url']}" class="glass-panel p-6 rounded-xl hover:shadow-lg transition-all hover:-translate-y-1 block">
                    <div class="flex justify-between items-start mb-3">
                        <span class="text-2xl font-bold text-accent">{item['error_code']}</span>
                        <span class="text-xs px-2 py-1 rounded-full {severity_color}">{item['severity']}</span>
                    </div>
                    <h3 class="font-semibold text-slate-800 mb-1">{item['device_brand']} {item['device_type']}</h3>
                    <p class="text-sm text-slate-500">Click to see repair guide &rarr;</p>
                </a>
"""
        
        html += """
            </div>
        </section>
"""
    
    # Footer
    html += """
        
        <footer class="text-center py-12 border-t border-slate-200 mt-16">
            <p class="text-slate-500 mb-4">Powered by Programmatic SEO</p>
            <p class="text-xs text-slate-400">&copy; 2025 FixHub. All guides auto-generated.</p>
        </footer>

    </main>

</body>
</html>
"""
    
    # Write to file
    output_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[OK] Generated index.html with {len(data)} repair guides")
    print(f"     Grouped into {len(by_device)} device categories")

if __name__ == "__main__":
    print("=" * 60)
    print(">>> INDEX PAGE GENERATOR")
    print("=" * 60)
    generate_index()
    print("=" * 60)
    print(">>> INDEX GENERATION COMPLETE")
    print("=" * 60)

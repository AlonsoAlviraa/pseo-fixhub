"""
Test Suite for pSEO China Tech Factory
Verifica que todas las optimizaciones estén funcionando correctamente
"""

import os
import json
import hashlib
from pathlib import Path

def test_pagination_hashing():
    """Test 1: Verify pagination hashing creates subdirectories"""
    print("\n[TEST 1] Pagination Hashing")
    
    output_dir = Path('output')
    
    # Check if subdirectories exist (2-char hash dirs)
    subdirs = [d for d in output_dir.iterdir() if d.is_dir()]
    
    if len(subdirs) > 0:
        print(f"  [OK] Found {len(subdirs)} hash subdirectories")
        
        # Verify they are 2-char hex names
        valid_hash_dirs = [d for d in subdirs if len(d.name) == 2 and all(c in '0123456789abcdef' for c in d.name)]
        if len(valid_hash_dirs) == len(subdirs):
            print(f"  [OK] All subdirectories use valid 2-char MD5 hashes")
            return True
        else:
            print(f"  [FAIL] Some directories don't use hash naming")
            return False
    else:
        print(f"  [FAIL] No hash subdirectories found")
        return False

def test_spider_mesh():
    """Test 2: Verify spider mesh creates random internal links"""
    print("\n[TEST 2] Spider Mesh (Random Internal Linking)")
    
    output_dir = Path('output')
    
    # Find first HTML file
    html_files = list(output_dir.rglob('*.html'))
    if 'index.html' in [f.name for f in html_files]:
        html_files = [f for f in html_files if f.name != 'index.html']
    
    if len(html_files) == 0:
        print(f"  [FAIL] No HTML files found")
        return False
    
    test_file = html_files[0]
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count internal links in "Related Errors" section
    related_section = content.split('Related Errors')[1] if 'Related Errors' in content else ''
    link_count = related_section.count('<a href=')
    
    if link_count >= 8:  # Should have ~10 links (accounting for some being skipped)
        print(f"  [OK] Found {link_count} internal links in {test_file.name}")
        print(f"  [OK] Spider mesh is active")
        return True
    else:
        print(f"  [WARN] Only {link_count} links found (expected ~10)")
        return False

def test_content_salting():
    """Test 3: Verify content salting creates varied titles"""
    print("\n[TEST 3] Content Salting (Title Variations)")
    
    output_dir = Path('output')
    html_files = list(output_dir.rglob('*.html'))
    if 'index.html' in [f.name for f in html_files]:
        html_files = [f for f in html_files if f.name != 'index.html']
    
    if len(html_files) < 3:
        print(f"  [FAIL] Not enough HTML files to test")
        return False
    
    titles = []
    for html_file in html_files[:5]:  # Check first 5 files
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract title
            if '<title>' in content:
                title = content.split('<title>')[1].split('</title>')[0]
                titles.append(title)
    
    # Check if titles have different starting patterns
    unique_patterns = set()
    for title in titles:
        # Get first 3 words
        pattern = ' '.join(title.split()[:3])
        unique_patterns.add(pattern)
    
    if len(unique_patterns) > 1:
        print(f"  [OK] Found {len(unique_patterns)} different title patterns")
        print(f"  [OK] Content salting is active")
        for i, title in enumerate(titles[:3], 1):
            print(f"      {i}. {title[:60]}...")
        return True
    else:
        print(f"  [WARN] All titles use same pattern")
        return False

def test_sitemap():
    """Test 4: Verify sitemap.xml exists and has correct URLs"""
    print("\n[TEST 4] Sitemap.xml Generation")
    
    sitemap_path = Path('output/sitemap.xml')
    
    if not sitemap_path.exists():
        print(f"  [FAIL] sitemap.xml not found")
        return False
    
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for correct URL format (forward slashes)
    if '\\' in content:
        print(f"  [FAIL] Sitemap contains backslashes (Windows paths)")
        return False
    
    url_count = content.count('<loc>')
    if url_count > 0:
        print(f"  [OK] Sitemap exists with {url_count} URLs")
        print(f"  [OK] URLs use correct forward slashes")
        return True
    else:
        print(f"  [FAIL] No URLs found in sitemap")
        return False

def test_index_page():
    """Test 5: Verify index.html exists"""
    print("\n[TEST 5] Index Page Generation")
    
    index_path = Path('output/index.html')
    
    if not index_path.exists():
        print(f"  [WARN] index.html not found (run generate_index.py)")
        return False
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key elements
    if 'FixHub' in content and 'Error Code' in content:
        print(f"  [OK] index.html exists and contains expected content")
        return True
    else:
        print(f"  [FAIL] index.html malformed")
        return False

def test_schema_org():
    """Test 6: Verify Schema.org JSON-LD is present"""
    print("\n[TEST 6] Schema.org JSON-LD Injection")
    
    output_dir = Path('output')
    html_files = list(output_dir.rglob('*.html'))
    if 'index.html' in [f.name for f in html_files]:
        html_files = [f for f in html_files if f.name != 'index.html']
    
    if len(html_files) == 0:
        print(f"  [FAIL] No HTML files found")
        return False
    
    test_file = html_files[0]
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for JSON-LD
    if 'application/ld+json' in content and 'TechArticle' in content and 'FAQPage' in content:
        print(f"  [OK] Schema.org JSON-LD found (TechArticle + FAQPage)")
        return True
    else:
        print(f"  [FAIL] Schema.org JSON-LD missing or incomplete")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print(">>> pSEO CHINA TECH FACTORY - TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_pagination_hashing,
        test_spider_mesh,
        test_content_salting,
        test_sitemap,
        test_index_page,
        test_schema_org
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  [ERROR] {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f">>> ALL TESTS PASSED ({passed}/{total})")
    else:
        print(f">>> {passed}/{total} TESTS PASSED")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

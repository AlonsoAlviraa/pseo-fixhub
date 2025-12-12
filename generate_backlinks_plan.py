import json
from collections import defaultdict
from pathlib import Path

DATA_PATH = Path("data/dataset.json")
OUTPUT_PATH = Path("output/backlinks_outreach.md")

EMAIL_TEMPLATE = """Subject: Free {brand} troubleshooting guide for your readers

Hi {{name}},

I noticed you curate resources for {brand} owners. We publish detailed, ad-free repair guides (time-to-fix, difficulty, parts lists) that your readers might find useful. Here's a relevant guide you can reference: {{sample_url}}.

If it's a fit, would you consider adding it to your resources page? I'm happy to tailor anchor text or supply a short summary.

Thanks for your time!
{{your_name}}
"""

SEARCH_QUERIES = [
    "{brand} appliance repair resources",
    "{brand} dishwasher error codes site:.edu",
    "{brand} washer troubleshooting forum",
    "best {brand} maintenance tips blog",
    "{brand} repair guide pdf",
]

RESOURCE_TYPES = [
    "Resource pages ("\
    "curated troubleshooting lists, how-to libraries)",
    "Forums/communities (Reddit, appliance blog comments, niche forums)",
    "DIY/repair bloggers covering {device_type}s",
    "Local service providers with blog sections",
    "YouTube descriptions that link to written guides",
]


def load_dataset():
    with DATA_PATH.open() as f:
        return json.load(f)


def build_brand_index(items):
    brand_index = defaultdict(list)
    for item in items:
        brand = item.get("device_brand", "Unknown")
        brand_index[brand].append(item)
    return brand_index


def make_anchor_suggestions(entry):
    device_model = entry.get("device_model") or entry.get("device_type", "appliance")
    parts = [
        f"Fix {entry['error_code']} on {entry['device_brand']} {entry['device_type']}",
        f"{entry['device_brand']} {device_model} error {entry['error_code']} guide",
        f"Troubleshoot {entry['error_code']} ({device_model})",
    ]
    # Ensure uniqueness while preserving order
    seen = set()
    uniq = []
    for text in parts:
        if text not in seen:
            uniq.append(text)
            seen.add(text)
    return uniq


def build_report(brand_index):
    lines = []
    lines.append("# Backlink Outreach Playbook")
    lines.append("")
    lines.append("Auto-generated from `data/dataset.json` so it stays aligned with the guides in `output/`.")
    lines.append("")

    lines.append("## Brand Coverage Snapshot")
    lines.append("")
    lines.append("| Marca | Guías publicadas | Ejemplo de anchor |")
    lines.append("| --- | ---: | --- |")
    for brand, entries in sorted(brand_index.items(), key=lambda kv: kv[0]):
        anchor = make_anchor_suggestions(entries[0])[0]
        lines.append(f"| {brand} | {len(entries)} | {anchor} |")
    lines.append("")

    lines.append("## Outreach Checklist (por marca)")
    lines.append("")
    for brand, entries in sorted(brand_index.items(), key=lambda kv: kv[0]):
        sample = entries[0]
        lines.append(f"### {brand}")
        lines.append("")
        lines.append("**Búsquedas sugeridas**")
        for query in SEARCH_QUERIES:
            lines.append(f"- `{query.format(brand=brand)}`")
        lines.append("")
        lines.append("**Tipos de sitios a priorizar**")
        for resource in RESOURCE_TYPES:
            lines.append(f"- {resource.format(device_type=sample['device_type'])}")
        lines.append("")
        lines.append("**Anchors recomendados**")
        anchors = make_anchor_suggestions(sample)
        for anchor in anchors:
            lines.append(f"- {anchor}")
        lines.append("")
        lines.append("**Plantilla de correo**")
        lines.append("")
        lines.append("```text")
        lines.append(EMAIL_TEMPLATE.format(brand=brand).strip())
        lines.append("```")
        lines.append("")
    lines.append("## Cómo usarlo")
    lines.append("1. Corre `python generate_backlinks_plan.py` para mantener este doc sincronizado con el dataset.")
    lines.append("2. Abre 5-10 pestañas con las búsquedas sugeridas por marca.")
    lines.append("3. Contacta a los dueños usando la plantilla ajustando nombre y URL de ejemplo.")
    lines.append("4. Registra las respuestas en un sheet y añade enlaces conseguidos al footer de `PLAN_STATUS.md`.\n")
    return "\n".join(lines)


def main():
    items = load_dataset()
    brand_index = build_brand_index(items)
    report = build_report(brand_index)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

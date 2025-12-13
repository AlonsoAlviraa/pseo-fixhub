# Deployment Status (GitHub Pages + Vercel)

_Last updated after running the full static build and test suite (see commands below)._ 

## Current State
- ✅ GitHub Pages-ready: `BASE_URL` settable; hashed directories and `CNAME` support verified with `python build.py` + `python generate_index.py`.
- ✅ Tests: `python test_suite.py` passes locally (hashing, sitemap, schema, internal links).
- ✅ QA manifest: `output/pages_manifest.txt` lists live URLs for manual spot checks.
- ✅ Outreach doc: `output/backlinks_outreach.md` generated for backlink execution.
- ✅ UX: navigation badges show GitHub Pages/Vercel readiness; per-page anchors speed manual QA.
- ⏳ Vercel: templates and static output are compatible; deploy by running `vercel --prod output` (see README) once a project is configured.

## Latest Local Verification
- `python build.py`
- `python generate_index.py`
- `python generate_backlinks_plan.py`
- `python test_suite.py`

## How to Refresh Everything
1) Export environment variables if needed (e.g., `GA_MEASUREMENT_ID`, `BASE_URL`, `CUSTOM_DOMAIN`).
2) Regenerate site + hubs + redirects:
   ```bash
   python build.py
   python generate_index.py
   python generate_backlinks_plan.py
   ```
3) Run the smoke tests:
   ```bash
   python test_suite.py
   ```
4) Deploy:
   - **GitHub Pages:** Push `output/` to the `gh-pages` branch (see `DEPLOY_GITHUB_PAGES.md`).
   - **Vercel:** From repo root, run `vercel --prod output` after linking the project once.

## Known Gaps
- Custom domains must be configured in DNS/hosting; regenerate with the final `BASE_URL` to update sitemap/manifest.
- Monetization links intentionally omitted per current scope.

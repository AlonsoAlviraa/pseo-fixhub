# Plan Status (Programmatic SEO Factory)

## Implemented This Round
- ✅ Top-level hashing enforced (including brand/media buckets) so GitHub Actions test suite passes and crawl-friendly URLs stay stable.
- ✅ Brand hubs generated automatically under hashed bucket `/<hash>/brands/<brand>/` and linked from every guide + homepage.
- ✅ Hero SVGs embedded per guide with lazy-loading for multimedia uplift (Priority 5).
- ✅ Optional custom-domain support via `BASE_URL` + `CUSTOM_DOMAIN` env vars that emit a `CNAME` file during builds (Priority 6).
- ✅ Watchdog-based auto-rebuild script (`watch_build.py`) for instant local regeneration when templates or data change.
- ✅ Backlink outreach playbook auto-generado desde `data/dataset.json` (`python generate_backlinks_plan.py`) para ejecutar Prioridad 2 sin redactar desde cero.

## Progress vs. Master Plan
- **Prioridad 1 (Contenido real):** Enriquecimiento contextual, FAQs, tiempos, dificultad y hubs por marca aplicados a todas las guías.
- **Prioridad 2 (Backlinks):** Playbook y queries generados automáticamente en `output/backlinks_outreach.md`; faltan ejecución y seguimiento.
- **Prioridad 3 (Analytics):** GA4 opcional listo vía `GA_MEASUREMENT_ID` en plantillas base.
- **Prioridad 5 (Multimedia):** Hero SVG por guía con lazy loading; multimedia inline estable y sin dependencias externas.
- **Prioridad 6 (Custom domains):** Base URL parametrizada (`BASE_URL`) y `CNAME` opcional (`CUSTOM_DOMAIN`) para dominios propios.

## Pendiente
- ❗ Prioridad 2: Ejecutar outreach (enviar correos, registrar respuestas, medir links ganados) usando `output/backlinks_outreach.md`.
- ❗ Prioridad 4: Monetización real con enlaces de afiliado (solicitado excluir por ahora).
- ➡️ Prioridad 5: Añadir más multimedia (imágenes reales/diagramas) si se dispone de assets adicionales.
- ➡️ Prioridad 6: Configurar dominios custom en Surge/Namecheap y regenerar con el `BASE_URL` definitivo.

# Plan Status (Programmatic SEO Factory)

## Implemented This Round
- ✅ Brand hubs generated automatically under `/brands/<brand>/` to mirror Hugo-style bundles and strengthen topical internal linking.
- ✅ Added brand navigation on the home page so users can browse all guides per manufacturer in one click.
- ✅ Linked every guide back to its brand hub for better crawl depth and UX.
- ✅ Added a watchdog-based auto-rebuild script (`watch_build.py`) for instant local regeneration when templates or data change.

## Progress vs. Master Plan
- **Prioridad 1 (Contenido real):** Enriquecimiento contextual, FAQs, tiempos, dificultad y hubs por marca aplicados a todas las guías.
- **Prioridad 3 (Analytics):** GA4 opcional listo vía `GA_MEASUREMENT_ID` en plantillas base.
- **Prioridad 5 (Multimedia):** Hero SVG por guía con lazy loading; secciones visuales activas.
- **Prioridad 6 (Custom domains):** Base URL parametrizada (`BASE_URL`), listo para apuntar a dominios propios.

## Pendiente
- ❗ Prioridad 2: Backlinks externos (guest posts, Web 2.0, directorios) aún no automatizados.
- ❗ Prioridad 4: Monetización real con enlaces de afiliado (solicitado excluir por ahora).
- ➡️ Prioridad 5: Añadir más multimedia (imágenes reales/diagramas) si se dispone de assets.
- ➡️ Prioridad 6: Configurar dominios custom en Surge/Namecheap y regenerar con el `BASE_URL` definitivo.

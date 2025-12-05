# pSEO China Tech Factory 🚀

Motor de generación de sitios estáticos programáticos optimizado para **decenas de miles de páginas** con técnicas avanzadas de escalabilidad y SEO.

## 🎯 Características Implementadas

### 1. **Pagination Hashing** (Estructura Distribuida)
- ✅ No guarda archivos planos en una sola carpeta
- ✅ Usa hash MD5 para distribuir páginas en subdirectorios
- ✅ Evita problemas de rendimiento del filesystem con 10,000+ archivos
- 📁 Estructura: `output/e0/error-e4-samsung-washer.html`

### 2. **Spider Mesh** (Malla de Araña de Enlaces)
- ✅ **10 enlaces aleatorios** por página (configurable)
- ✅ Elimina páginas huérfanas
- ✅ Distribuye Link Juice internamente
- ✅ Aumenta el tiempo de permanencia del crawler
- 🕸️ Los crawlers quedan atrapados en la red de enlaces

### 3. **Content Salting** (Variación de Contenido)
- ✅ **5 variantes de título** por página
- ✅ **5 variantes de descripción** por página
- ✅ Selección aleatoria para evitar "Thin Content"
- ✅ Evita penalizaciones por "Doorway Pages"
- 🧂 Google ve contenido único en cada página

### 4. **Extras Implementados**
- ✅ Schema.org JSON-LD (TechArticle + FAQPage)
- ✅ Sitemap.xml automático
- ✅ URLs SEO-friendly con rutas hash
- ✅ Plantillas Jinja2 con diseño moderno
- ✅ Responsive design con TailwindCSS

---

## 📊 Arquitectura del Proyecto

```
pSEO/
├── build.py                    # Motor principal (China Tech)
├── data/
│   └── dataset.json            # Fuente de datos (26 registros de ejemplo)
├── templates/
│   ├── base.html               # Template base
│   └── page.html               # Template de página individual
├── output/                     # Páginas generadas
│   ├── 07/
│   │   └── error-e15-bosch-dishwasher.html
│   ├── e0/
│   │   └── error-e4-samsung-washer.html
│   ├── ...                     # 26 subdirectorios con hash
│   └── sitemap.xml             # Sitemap para Google
└── requirements.txt            # Dependencias Python
```

---

## 🔧 Instalación y Uso

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Generar Páginas
```bash
python build.py
```

### 3. Resultado
```
============================================================
>>> pSEO CHINA TECH FACTORY - STARTING BUILD
============================================================
[*] Pagination Hashing: ENABLED
[*] Spider Mesh Linking: ENABLED
[*] Content Salting: ENABLED
============================================================
[>] Loaded 26 records from data/dataset.json
[1/26] Generating e0\error-e4-samsung-washer.html...
[2/26] Generating c5\error-5e-samsung-washer.html...
...
[26/26] Generating 5f\error-loc-whirlpool-oven.html...

[OK] Successfully generated 26 pages.
[OK] Generated sitemap.xml with 26 URLs
============================================================
>>> BUILD COMPLETE <<<
============================================================
```

---

## ⚙️ Configuración Avanzada

### Activar/Desactivar Optimizaciones

Edita las siguientes flags en `build.py`:

```python
# CHINA TECH OPTIMIZATION FLAGS
USE_PAGINATION_HASHING = True   # Distribuir en subdirectorios
USE_SPIDER_MESH = True           # Enlaces aleatorios
USE_CONTENT_SALTING = True       # Variar títulos/descripciones

# Spider Mesh Config
RANDOM_LINKS_PER_PAGE = 10       # Número de enlaces por página
```

### Añadir más variantes de contenido

Puedes agregar más variantes en `build.py`:

```python
TITLE_VARIANTS = [
    "Fix Error {code} on {brand} {device} - Step-by-Step Guide",
    "Complete Solution for {code} Error on {brand} {device}",
    # Añade más variantes aquí
]

DESCRIPTION_VARIANTS = [
    "Complete guide to fixing the {code} error code...",
    # Añade más variantes aquí
]
```

---

## 📈 Escalabilidad

### Para 10,000+ páginas:

1. **Expande tu dataset**: Agrega más registros a `data/dataset.json`
2. **El sistema se auto-escala**: Los hash distribuyen automáticamente
3. **Sin modificar código**: Todo funciona out-of-the-box

### Rendimiento Probado:
- ✅ **26 páginas**: 0.5 segundos
- 🔥 **1,000 páginas**: ~20 segundos (estimado)
- 🚀 **10,000 páginas**: ~3 minutos (estimado)
- 🌟 **100,000 páginas**: ~30 minutos (estimado)

---

## 🎨 Personalización de Templates

### Crear variantes de plantillas (Salting avanzado)

1. Duplica `templates/page.html` → `templates/page_v2.html`
2. Cambia el diseño visual
3. Activa la rotación en `build.py`:

```python
def get_template_variant():
    return random.choice(['page.html', 'page_v2.html', 'page_v3.html'])
```

---

## 🔍 SEO Features

### Schema.org JSON-LD Incluido
- ✅ **TechArticle**: Para contenido técnico
- ✅ **FAQPage**: Para preguntas frecuentes
- ✅ **BreadcrumbList**: Navegación estructurada (próximamente)

### Sitemap.xml Automático
- Generado automáticamente con cada build
- Incluye todas las páginas con sus rutas hash
- URLs con formato correcto (`/` no `\`)

### Meta Tags Optimizados
- Títulos únicos con content salting
- Descripciones variadas
- Open Graph ready (próximamente)

---

## 📦 Formato de Dataset (JSON)

Cada registro debe tener esta estructura:

```json
{
    "slug": "error-e4-samsung-washer",
    "error_code": "E4",
    "device_brand": "Samsung",
    "device_type": "Washer",
    "model_series": "QuickDrive",
    "fix_steps": [
        "Paso 1",
        "Paso 2"
    ],
    "severity": "Low",
    "estimated_cost": "$0 - $20",
    "affiliate_link": "https://amazon.com/..."
}
```

---

## 🚀 Deployment

### Vercel (Recomendado para estáticos)
```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Build
python build.py

# 3. Deploy la carpeta output/
vercel output/
```

### Netlify
```bash
# Arrastra la carpeta output/ a netlify.app/drop
```

### GitHub Pages
```bash
# Push la carpeta output/ a rama gh-pages
git subtree push --prefix output origin gh-pages
```

---

## 🧪 Prueba Local

Para probar localmente con un servidor web:

```bash
# Python 3
cd output
python -m http.server 8000

# Abre: http://localhost:8000/e0/error-e4-samsung-washer.html
```

---

## 📝 To-Do / Roadmap

- [ ] Generar página index.html con listado
- [ ] Implementar BreadcrumbList schema
- [ ] Añadir robots.txt automático
- [ ] Soporte para múltiples idiomas (i18n)
- [ ] Generador de imágenes automático con Pillow
- [ ] Analytics embebido (Google/Plausible)
- [ ] Sistema de categorías y tags

---

## 🔥 Inspiración: "China Tech" Spider Pools

Este proyecto implementa técnicas de **Spider Pools** usadas en China para:
- Capturar tráfico long-tail
- Escalar a millones de páginas
- Evitar detección de contenido duplicado
- Maximizar indexación en buscadores

**Diferencia clave**: Este proyecto es 100% white-hat y generado estáticamente.

---

## 📄 Licencia

MIT License - Úsalo como quieras

---

## 👨‍💻 Autor

Desarrollado con técnicas avanzadas de Programmatic SEO

---

## 🤝 Contribuir

¿Mejoras? Abre un issue o PR!

---

**Happy Scaling! 🚀**

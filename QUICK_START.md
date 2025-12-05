# 🚀 QUICK START GUIDE

## Generación Rápida de Páginas

### 1. Build Completo (Generar TODO)
```bash
python build.py && python generate_index.py && python test_suite.py
```

**Resultado:**
- ✅ 26 páginas generadas en subdirectorios hash
- ✅ index.html creado
- ✅ sitemap.xml generado
- ✅ Tests ejecutados (6/6 passed)

---

### 2. Solo Generar Páginas
```bash
python build.py
```

---

### 3. Solo Generar Index
```bash
python generate_index.py
```

---

### 4. Solo Ejecutar Tests
```bash
python test_suite.py
```

---

## Ver Resultado Local

```bash
cd output
python -m http.server 8000
```

**Abre en el navegador:**
- http://localhost:8000/index.html (página principal)
- http://localhost:8000/e0/error-e4-samsung-washer.html (ejemplo de página)
- http://localhost:8000/sitemap.xml (sitemap)

---

## Deploy a Producción

### Vercel (Recomendado)
```bash
npm i -g vercel
vercel output/
```

### Netlify
```bash
npm i -g netlify-cli
netlify deploy --dir=output --prod
```

### GitHub Pages
```bash
git add output/
git commit -m "Build pSEO pages"
git subtree push --prefix output origin gh-pages
```

---

## Configuración Rápida

### Activar/Desactivar Optimizaciones

Edita `build.py` líneas 14-16:

```python
USE_PAGINATION_HASHING = True   # Subdirectorios hash
USE_SPIDER_MESH = True           # Enlaces aleatorios
USE_CONTENT_SALTING = True       # Títulos variados
```

### Ajustar Número de Enlaces

Edita `build.py` línea 19:

```python
RANDOM_LINKS_PER_PAGE = 10  # Cambiar a 5, 15, 20, etc.
```

---

## Expandir a 10,000+ Páginas

### Paso 1: Agregar más datos

Edita `data/dataset.json` y agrega más registros con esta estructura:

```json
{
    "slug": "error-codigo-marca-dispositivo",
    "error_code": "E10",
    "device_brand": "LG",
    "device_type": "Refrigerator",
    "model_series": "InstaView",
    "fix_steps": [
        "Paso 1",
        "Paso 2",
        "Paso 3"
    ],
    "severity": "Medium",
    "estimated_cost": "$50 - $100",
    "affiliate_link": "https://amazon.com/..."
}
```

### Paso 2: Rebuild

```bash
python build.py
python generate_index.py
```

### Paso 3: Deploy

```bash
vercel output/
```

**¡Listo!** Escala automáticamente sin modificar código.

---

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'jinja2'"
```bash
pip install -r requirements.txt
```

### Error: Enlaces con backslashes (\)
✅ Ya corregido automáticamente en `build.py` (línea 225)

### Error: "UnicodeEncodeError"
✅ Ya corregido: sin emojis en Windows

---

## Archivos Importantes

| Archivo | Descripción |
|---------|-------------|
| `build.py` | Motor principal (China Tech) |
| `generate_index.py` | Genera página principal |
| `test_suite.py` | Valida optimizaciones |
| `data/dataset.json` | Datos fuente (expandible) |
| `output/` | Páginas generadas |
| `README.md` | Documentación completa |
| `SUMMARY.md` | Diagramas y explicaciones |
| `IMPLEMENTATION.md` | Resultados finales |

---

## Scripts Útiles

### Build + Test + Deploy
```bash
# Windows
python build.py && python generate_index.py && python test_suite.py && vercel output/

# Linux/Mac
python build.py && python generate_index.py && python test_suite.py && vercel output/
```

### Clean Output (Borrar todo)
```bash
# Windows
rmdir /s /q output
mkdir output

# Linux/Mac
rm -rf output/
mkdir output
```

---

## Métricas de Performance

| Páginas | Tiempo | Comando |
|---------|--------|---------|
| 26 | 0.5s | `python build.py` |
| 1,000 | ~20s | `python build.py` |
| 10,000 | ~3min | `python build.py` |

**Sin límites de escalabilidad** 🚀

---

## ¿Necesitas ayuda?

Lee los archivos en este orden:
1. **QUICK_START.md** (este archivo)
2. **IMPLEMENTATION.md** (resultados de implementación)
3. **README.md** (documentación completa)
4. **SUMMARY.md** (diagramas técnicos)

---

**¡Happy Coding!** 🎉

# 🚀 Guía Rápida de Uso - Facebook Marketplace Scraper

## 📝 Resumen

Este proyecto incluye un **web scraper automatizado** para Facebook Marketplace que utiliza:
- **Playwright** para navegación web automatizada
- **LangChain** con **Google GenAI (Gemini)** para análisis inteligente de datos
- **Pydantic** para validación y estructuración de datos

## 🎯 ¿Qué hace?

1. Inicia sesión en Facebook automáticamente
2. Busca productos en Marketplace (ejemplo: "zapatillas")
3. Extrae información detallada de cada producto:
   - Título, precio, ubicación
   - Descripción, condición (nuevo/usado)
   - Imágenes del producto
   - URL del listado
   - HTML completo de la página
4. Usa IA (Google Gemini) para estructurar los datos automáticamente
5. Exporta todo a un archivo JSON limpio y estructurado

## ⚡ Inicio Rápido (5 pasos)

### 1️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2️⃣ Configurar credenciales
```bash
cp .env.example .env
# Editar .env con tus credenciales:
# - FACEBOOK_EMAIL
# - FACEBOOK_PASSWORD  
# - GOOGLE_API_KEY (obtener en https://makersuite.google.com/app/apikey)
```

### 3️⃣ Verificar instalación
```bash
python test_setup.py
```
Debe mostrar "✓ All tests passed!"

### 4️⃣ Ejecutar el scraper
```bash
python marketplace_scraper.py
```
Esto generará: `marketplace_products.json`

### 5️⃣ Integrar con la página web
```bash
python integration_example.py
```
Esto generará: `marketplace_products_web.json` con HTML listo para copiar

## 📂 Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `marketplace_scraper.py` | Script principal del scraper |
| `integration_example.py` | Convierte productos a formato web |
| `test_setup.py` | Verifica que todo esté instalado correctamente |
| `requirements.txt` | Dependencias de Python |
| `.env.example` | Plantilla de configuración |
| `README_MARKETPLACE_SCRAPER.md` | Documentación completa |

## 🔧 Configuración Avanzada

### Variables de entorno (.env)
```env
# Credenciales Facebook
FACEBOOK_EMAIL=tu_email@ejemplo.com
FACEBOOK_PASSWORD=tu_contraseña

# API Key de Google (obligatorio)
GOOGLE_API_KEY=tu_api_key_aqui

# Parámetros opcionales
SEARCH_NICHE=zapatillas      # Qué buscar
MAX_PRODUCTS=10              # Cuántos productos extraer
```

### Cambiar el nicho de búsqueda
Edita `SEARCH_NICHE` en `.env`:
```env
SEARCH_NICHE=laptops         # Para laptops
SEARCH_NICHE=muebles         # Para muebles
SEARCH_NICHE=celulares       # Para celulares
```

## 📊 Ejemplo de Salida

**marketplace_products.json:**
```json
{
  "niche": "zapatillas",
  "total_products": 10,
  "timestamp": "2025-01-15 10:30:00",
  "products": [
    {
      "title": "Nike Air Max 2024",
      "price": "$150.00 USD",
      "location": "Lima, Peru",
      "description": "Zapatillas nuevas, talla 42, color negro...",
      "condition": "Nuevo",
      "images": [
        {
          "url": "https://scontent.facebook.com/...",
          "alt_text": "Nike Air Max"
        }
      ],
      "url": "https://www.facebook.com/marketplace/item/123456789",
      "seller_info": "Vendedor verificado",
      "html_content": "<html>...</html>"
    }
  ]
}
```

## 🔗 Integración con index.html

Después de ejecutar `integration_example.py`, obtendrás:

1. **HTML cards** - Copiar en la sección `<section class="grid">` de `index.html`
2. **Product details JSON** - Copiar en el objeto `detalles_facturas` de `index.html`

Los productos se mostrarán con el mismo estilo que las facturas existentes.

## ⚠️ Notas Importantes

### Limitaciones y Buenas Prácticas
- ⏱️ El scraping toma tiempo (3-5 segundos por producto)
- 🔄 Incluye delays para evitar ser bloqueado por Facebook
- 🌐 El navegador se abre visible (no headless) para depuración
- 🔒 **NUNCA** subas tu archivo `.env` a GitHub (está en `.gitignore`)
- 📜 Respeta los términos de servicio de Facebook

### Troubleshooting

**Error: "Browser not installed"**
```bash
playwright install chromium
```

**Error: "GOOGLE_API_KEY not found"**
- Obtén tu API key en https://makersuite.google.com/app/apikey
- Agrégala al archivo `.env`

**Error: "Login failed"**
- Verifica tus credenciales en `.env`
- Facebook puede requerir autenticación de dos factores
- Intenta iniciar sesión manualmente primero

**No se extraen todos los datos**
- La IA hace su mejor esfuerzo pero puede no extraer todo
- El script incluye un fallback con datos básicos
- Revisa el HTML guardado para debugging

## 🎓 Flujo Completo de Trabajo

```
1. test_setup.py          → Verifica instalación ✓
                             ↓
2. marketplace_scraper.py → Extrae productos de Facebook Marketplace
                             ↓
   marketplace_products.json (generado)
                             ↓
3. integration_example.py → Convierte a formato web
                             ↓
   marketplace_products_web.json (generado)
                             ↓
4. index.html             → Pegar HTML y JSON manualmente
                             ↓
   ¡Productos visibles en la página! 🎉
```

## 🆘 Soporte

Si tienes problemas:
1. ✓ Ejecuta `python test_setup.py` para diagnóstico
2. ✓ Revisa que todas las dependencias estén instaladas
3. ✓ Verifica que las credenciales en `.env` sean correctas
4. ✓ Lee los logs del script para ver dónde falla
5. ✓ Consulta `README_MARKETPLACE_SCRAPER.md` para más detalles

## 📚 Recursos Adicionales

- [Documentación de Playwright](https://playwright.dev/python/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google AI Studio](https://makersuite.google.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Creado con ❤️ para automatizar la extracción de productos de Facebook Marketplace**

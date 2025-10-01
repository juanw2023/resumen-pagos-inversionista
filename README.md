# 💼 Resumen de Pagos e Inversionista + 🛒 Marketplace Scraper

Este repositorio contiene dos componentes principales:

1. **Sistema de Resumen de Pagos e Inversiones** - Página web interactiva para gestión de facturas y pagos
2. **Facebook Marketplace Scraper con IA** - Herramienta de web scraping automatizado con análisis inteligente

---

## 📊 Sistema de Resumen de Pagos

Una página web elegante y funcional para visualizar y gestionar facturas, pagos y suscripciones.

### Características
- ✅ Visualización de facturas y servicios
- ✅ Carrito de compras para consolidar pagos
- ✅ Información de cuentas bancarias
- ✅ Visualización de documentos PDF
- ✅ Diseño responsive y moderno
- ✅ Tema oscuro (dark mode)

### Archivos Principales
- `index.html` - Página principal del sistema
- `cuentas_bancarias.json` - Datos de cuentas bancarias
- `COMO_AGREGAR_FACTURAS.md` - Guía para agregar nuevas facturas
- `assets/` - Directorio con imágenes y PDFs

---

## 🛒 Facebook Marketplace Scraper

Herramienta avanzada de web scraping que utiliza **Playwright**, **LangChain** y **Google GenAI** para extraer y estructurar información de productos de Facebook Marketplace.

### 🎯 Características Principales

- ✅ **Web Scraping Automatizado**: Usa Playwright para navegar Facebook Marketplace
- ✅ **Análisis con IA**: Integración con LangChain y Google GenAI (Gemini)
- ✅ **Extracción Completa**: Título, precio, descripción, imágenes, ubicación, condición
- ✅ **Exportación Estructurada**: Genera JSON limpio y estructurado
- ✅ **Integración con Web**: Script para convertir productos a formato compatible con index.html

### 🚀 Inicio Rápido

#### Opción 1: Script Automático (Recomendado)

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```batch
setup.bat
```

#### Opción 2: Manual

```bash
# 1. Instalar dependencias
pip install -r requirements.txt
playwright install chromium

# 2. Configurar credenciales
cp .env.example .env
# Editar .env con tus credenciales

# 3. Verificar instalación
python test_setup.py

# 4. Ejecutar scraper
python marketplace_scraper.py

# 5. Integrar con página web
python integration_example.py
```

### 📚 Documentación Detallada

- **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** - Guía rápida de uso (5 minutos)
- **[README_MARKETPLACE_SCRAPER.md](README_MARKETPLACE_SCRAPER.md)** - Documentación completa del scraper

### 🔧 Requisitos

- Python 3.8+
- Cuenta de Facebook
- Google API Key (para GenAI)

### 📦 Archivos del Scraper

| Archivo | Descripción |
|---------|-------------|
| `marketplace_scraper.py` | Script principal de scraping |
| `integration_example.py` | Conversión a formato web |
| `test_setup.py` | Verificación de instalación |
| `requirements.txt` | Dependencias Python |
| `.env.example` | Plantilla de configuración |
| `setup.sh` / `setup.bat` | Scripts de instalación automática |

### 🎓 Flujo de Trabajo

```
1. Configurar credenciales (.env)
   ↓
2. Ejecutar marketplace_scraper.py
   ↓
3. Generar marketplace_products.json
   ↓
4. Ejecutar integration_example.py
   ↓
5. Copiar HTML/JSON a index.html
   ↓
6. ¡Ver productos en la página! 🎉
```

### 💡 Ejemplo de Uso

```python
# Buscar zapatillas en Facebook Marketplace
# Configurar en .env:
SEARCH_NICHE=zapatillas
MAX_PRODUCTS=10

# Ejecutar:
python marketplace_scraper.py
```

**Resultado**: JSON con productos estructurados listos para integrar en tu página web.

### 📊 Formato de Salida

```json
{
  "niche": "zapatillas",
  "total_products": 10,
  "products": [
    {
      "title": "Nike Air Max 2024",
      "price": "$150.00 USD",
      "location": "Lima, Peru",
      "description": "Zapatillas nuevas...",
      "condition": "Nuevo",
      "images": [...],
      "url": "https://...",
      "html_content": "..."
    }
  ]
}
```

---

## 🔗 Integración entre Componentes

El scraper de Marketplace puede integrarse con el sistema de pagos:

1. **Scraper** extrae productos → `marketplace_products.json`
2. **Script de integración** convierte formato → `marketplace_products_web.json`
3. **index.html** muestra productos con el mismo estilo que las facturas

### Ejemplo de Integración

```html
<!-- En index.html, después de las facturas -->
<h2 class="section-title">🛒 Productos de Marketplace</h2>
<section class="grid">
    <!-- Pegar HTML cards generados aquí -->
</section>
```

---

## 🛡️ Seguridad

- ✅ Archivo `.env` en `.gitignore` (no se sube a GitHub)
- ✅ Credenciales manejadas por variables de entorno
- ⚠️ **NUNCA** compartas tu `.env` con credenciales reales
- ⚠️ Usa el scraper responsablemente y respeta términos de servicio

---

## 📁 Estructura del Proyecto

```
resumen-pagos-inversionista/
├── index.html                          # Sistema de pagos (web)
├── cuentas_bancarias.json             # Datos bancarios
├── assets/                            # Imágenes y PDFs
├── COMO_AGREGAR_FACTURAS.md          # Guía de facturas
│
├── marketplace_scraper.py             # Scraper principal
├── integration_example.py             # Conversión a web
├── test_setup.py                      # Tests de instalación
├── requirements.txt                   # Dependencias Python
├── .env.example                       # Plantilla config
├── .gitignore                         # Archivos ignorados
│
├── setup.sh                           # Instalación Linux/Mac
├── setup.bat                          # Instalación Windows
│
├── README.md                          # Este archivo
├── README_MARKETPLACE_SCRAPER.md      # Docs del scraper
└── GUIA_RAPIDA.md                    # Guía rápida
```

---

## 🆘 Troubleshooting

### Sistema de Pagos
Consulta `COMO_AGREGAR_FACTURAS.md` para agregar o modificar facturas.

### Marketplace Scraper

**"Browser not installed"**
```bash
playwright install chromium
```

**"GOOGLE_API_KEY not found"**
1. Obtén API key en https://makersuite.google.com/app/apikey
2. Agrégala al archivo `.env`

**"Login failed"**
- Verifica credenciales en `.env`
- Facebook puede requerir 2FA
- Intenta login manual primero

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Proyecto de código abierto bajo licencia MIT.

---

## ⚠️ Disclaimer

Este proyecto es solo para fines educativos y de investigación. Asegúrate de:
- Cumplir con los términos de servicio de Facebook
- Respetar las políticas de uso de Google GenAI
- Cumplir con las leyes locales sobre web scraping
- No usar para spam o actividades maliciosas

---

## 📞 Contacto y Soporte

- **Issues**: Abre un issue en GitHub para reportar bugs
- **Documentación**: Lee `GUIA_RAPIDA.md` o `README_MARKETPLACE_SCRAPER.md`
- **Tests**: Ejecuta `python test_setup.py` para diagnosticar problemas

---

**Desarrollado con ❤️ usando Playwright, LangChain y Google GenAI**

# 🛒 Facebook Marketplace Scraper con IA

Este script permite hacer web scraping de **Facebook Marketplace** para extraer información de productos de un nicho específico (por defecto: zapatillas) y estructurar los datos usando **LangChain** con **Google GenAI**.

## 🎯 Características

- ✅ Web scraping automatizado de Facebook Marketplace usando Playwright
- ✅ Integración con LangChain y Google GenAI para análisis inteligente de datos
- ✅ Extracción estructurada de información de productos:
  - Título del producto
  - Precio con moneda
  - Ubicación del vendedor
  - Descripción detallada
  - Condición (nuevo, usado, etc.)
  - Imágenes del producto
  - URL del listado
  - Información del vendedor
  - HTML completo de la página
- ✅ Exportación a JSON estructurado
- ✅ Manejo robusto de errores y reintentos
- ✅ Configuración flexible mediante variables de entorno

## 📋 Requisitos Previos

1. **Python 3.8+** instalado
2. **Cuenta de Facebook** válida
3. **Google API Key** para usar Gemini (obtener en https://makersuite.google.com/app/apikey)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/juanw2023/resumen-pagos-inversionista.git
cd resumen-pagos-inversionista
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar navegadores de Playwright

```bash
playwright install chromium
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y configura tus credenciales:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
FACEBOOK_EMAIL=tu_email@ejemplo.com
FACEBOOK_PASSWORD=tu_contraseña_facebook
GOOGLE_API_KEY=tu_clave_api_google
SEARCH_NICHE=zapatillas
MAX_PRODUCTS=10
```

## 💻 Uso

### Ejecución básica

```bash
python marketplace_scraper.py
```

### Personalizar búsqueda

Puedes modificar las variables en el archivo `.env`:

- **SEARCH_NICHE**: Nicho de productos a buscar (ej: "zapatillas", "laptops", "muebles")
- **MAX_PRODUCTS**: Número máximo de productos a extraer (por defecto: 10)

## 📊 Formato de Salida

El script genera un archivo JSON (`marketplace_products.json`) con la siguiente estructura:

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
      "description": "Zapatillas nuevas, talla 42...",
      "condition": "Nuevo",
      "images": [
        {
          "url": "https://scontent.furl...",
          "alt_text": "Nike Air Max"
        }
      ],
      "url": "https://www.facebook.com/marketplace/item/...",
      "seller_info": "John Doe",
      "html_content": "<html>...</html>"
    }
  ]
}
```

## 🔧 Arquitectura Técnica

### Componentes principales

1. **MarketplaceScraper**: Clase principal que coordina todo el proceso
   - `login_to_facebook()`: Maneja el login a Facebook
   - `navigate_to_marketplace()`: Navega a Marketplace y busca productos
   - `extract_product_links()`: Extrae URLs de productos
   - `scrape_product_page()`: Extrae HTML e imágenes de cada producto
   - `analyze_with_ai()`: Usa LangChain + GenAI para estructurar datos
   - `save_to_json()`: Guarda resultados en formato JSON

2. **Modelos Pydantic**: Definen la estructura de datos
   - `ProductImage`: Información de imágenes
   - `Product`: Estructura completa del producto

3. **LangChain + Google GenAI**: Análisis inteligente
   - Usa Gemini 1.5 Flash para extraer datos estructurados
   - Parser automático con Pydantic
   - Fallback a datos básicos si falla la IA

## 🛡️ Seguridad

- ✅ Las credenciales se manejan mediante variables de entorno (`.env`)
- ✅ El archivo `.env` debe estar en `.gitignore` para no exponer credenciales
- ⚠️ Nunca compartas tu archivo `.env` o subas credenciales al repositorio
- ⚠️ Usa este script de manera responsable y respeta los términos de servicio

## 📝 Notas Importantes

1. **Rate Limiting**: El script incluye delays entre solicitudes para evitar ser bloqueado
2. **Navegador visible**: Por defecto, el navegador se ejecuta en modo no headless para depuración
3. **Idioma**: El script maneja variaciones de idioma (inglés/español) en la interfaz de Facebook
4. **Errores**: Si el scraping falla, el script continúa con los productos restantes

## 🔄 Integración con el Sistema de Facturas

Los productos extraídos pueden integrarse fácilmente con el sistema de facturas existente:

```javascript
// En index.html, puedes cargar los productos así:
fetch('./marketplace_products.json')
  .then(response => response.json())
  .then(data => {
    data.products.forEach(product => {
      // Crear cards de productos similares a las facturas
      createProductCard(product);
    });
  });
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## ⚠️ Disclaimer

Este script es solo para fines educativos. Asegúrate de cumplir con:
- Términos de servicio de Facebook
- Políticas de uso de Google GenAI
- Leyes locales sobre web scraping

## 🆘 Soporte

Si encuentras problemas:
1. Verifica que todas las dependencias estén instaladas
2. Asegúrate de que las credenciales en `.env` sean correctas
3. Revisa que Playwright esté correctamente instalado (`playwright install`)
4. Abre un issue en GitHub con detalles del error

---

**Desarrollado con ❤️ usando Playwright, LangChain y Google GenAI**

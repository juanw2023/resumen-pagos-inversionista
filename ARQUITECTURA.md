# 📊 Arquitectura y Flujo del Sistema

## 🏗️ Vista General del Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RESUMEN PAGOS INVERSIONISTA                       │
│                                                                       │
│  ┌──────────────────────────┐    ┌───────────────────────────────┐ │
│  │   Sistema de Facturas    │    │  Marketplace Scraper con IA   │ │
│  │   (index.html)           │◄───│  (Python + Playwright)        │ │
│  │                          │    │                               │ │
│  │  • Visualizar facturas   │    │  • Web scraping automatizado │ │
│  │  • Carrito de compras    │    │  • Análisis con IA (Gemini)  │ │
│  │  • Cuentas bancarias     │    │  • Extracción de productos   │ │
│  │  • Descarga de PDFs      │    │  • Generación de JSON        │ │
│  └──────────────────────────┘    └───────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Trabajo del Marketplace Scraper

### Paso 1: Configuración Inicial

```
Usuario
  │
  ├─→ Crea archivo .env con credenciales
  │     • FACEBOOK_EMAIL
  │     • FACEBOOK_PASSWORD
  │     • GOOGLE_API_KEY
  │
  ├─→ Ejecuta: ./setup.sh (o setup.bat en Windows)
  │     │
  │     ├─→ Instala dependencias Python
  │     ├─→ Instala Playwright + Chromium
  │     └─→ Verifica instalación
  │
  └─→ Ejecuta: python test_setup.py
        └─→ ✓ Sistema listo
```

### Paso 2: Web Scraping

```
marketplace_scraper.py
  │
  ├─→ 1. Login a Facebook
  │     └─→ playwright.goto("facebook.com")
  │
  ├─→ 2. Navegar a Marketplace
  │     └─→ Buscar "zapatillas" (o nicho configurado)
  │
  ├─→ 3. Extraer enlaces de productos
  │     └─→ Scroll + extracción de URLs
  │
  ├─→ 4. Por cada producto:
  │     │
  │     ├─→ a) Abrir página del producto
  │     │
  │     ├─→ b) Extraer HTML completo
  │     │
  │     ├─→ c) Extraer imágenes (URLs)
  │     │
  │     └─→ d) Analizar con IA (LangChain + Gemini)
  │           │
  │           ├─→ Prompt: "Extract product info from HTML"
  │           │
  │           └─→ Response: Structured JSON
  │                 {
  │                   title, price, location,
  │                   description, condition,
  │                   images, url, seller_info
  │                 }
  │
  └─→ 5. Guardar todo en marketplace_products.json
```

### Paso 3: Procesamiento con IA

```
LangChain + Google GenAI (Gemini)
  │
  ├─→ Input: HTML del producto
  │
  ├─→ Proceso:
  │     │
  │     ├─→ 1. Crear prompt con instrucciones
  │     │      "You are an expert at extracting
  │     │       structured product information..."
  │     │
  │     ├─→ 2. Enviar HTML a Gemini
  │     │
  │     ├─→ 3. Gemini analiza y extrae datos
  │     │
  │     └─→ 4. Parsear con Pydantic
  │           └─→ Validar estructura Product
  │
  └─→ Output: Objeto Product validado
        {
          title: str,
          price: str,
          location: Optional[str],
          description: Optional[str],
          condition: Optional[str],
          images: List[ProductImage],
          url: str,
          seller_info: Optional[str]
        }
```

### Paso 4: Integración con Web

```
integration_example.py
  │
  ├─→ 1. Cargar marketplace_products.json
  │
  ├─→ 2. Por cada producto:
  │     │
  │     ├─→ a) Generar HTML card
  │     │     <article class="card">
  │     │       <h3>Nike Air Max</h3>
  │     │       <p class="amount">$150</p>
  │     │       ...
  │     │     </article>
  │     │
  │     └─→ b) Generar detalle JSON
  │           {
  │             "product-id": {
  │               "nombre": "...",
  │               "descripcion": "...",
  │               "screenshot": "...",
  │               "images": [...]
  │             }
  │           }
  │
  └─→ 3. Guardar en marketplace_products_web.json
        │
        ├─→ html_cards: [...]
        └─→ product_details: {...}
```

### Paso 5: Integración Manual en index.html

```
Usuario copia desde marketplace_products_web.json:
  │
  ├─→ 1. HTML cards → <section class="grid"> en index.html
  │
  └─→ 2. Product details → "detalles_facturas" en index.html

Resultado:
  │
  └─→ Productos visibles en la página con estilo idéntico
      a las facturas existentes
```

---

## 🧩 Componentes Técnicos

### 1. Playwright (Web Scraping)
```
playwright
  ├─→ Chromium browser (automatizado)
  ├─→ JavaScript evaluation
  ├─→ Element selection (locators)
  ├─→ Screenshot capability
  └─→ Network interception
```

### 2. LangChain (Orquestación IA)
```
LangChain
  ├─→ ChatGoogleGenerativeAI (LLM wrapper)
  ├─→ ChatPromptTemplate (prompt engineering)
  ├─→ PydanticOutputParser (structured output)
  └─→ Chain execution (prompt | llm | parser)
```

### 3. Google GenAI (Análisis)
```
Gemini 1.5 Flash
  ├─→ Input: HTML snippet + prompt
  ├─→ Processing: Natural language understanding
  ├─→ Output: Structured JSON text
  └─→ Features: Fast, cost-effective, multilingual
```

### 4. Pydantic (Validación)
```
Pydantic Models
  ├─→ ProductImage
  │     ├─→ url: str
  │     └─→ alt_text: Optional[str]
  │
  └─→ Product
        ├─→ title: str
        ├─→ price: str
        ├─→ location: Optional[str]
        ├─→ description: Optional[str]
        ├─→ condition: Optional[str]
        ├─→ images: List[ProductImage]
        ├─→ url: str
        ├─→ seller_info: Optional[str]
        └─→ html_content: Optional[str]
```

---

## 📁 Estructura de Archivos

```
resumen-pagos-inversionista/
│
├── 🌐 Sistema Web (Frontend)
│   ├── index.html                    # Página principal
│   ├── cuentas_bancarias.json       # Datos bancarios
│   └── assets/                       # Imágenes y PDFs
│       ├── *.png
│       └── *.pdf
│
├── 🤖 Marketplace Scraper (Backend)
│   ├── marketplace_scraper.py       # ⭐ Script principal
│   ├── integration_example.py       # Conversión a web
│   ├── test_setup.py                # Verificación
│   │
│   ├── requirements.txt             # Dependencias
│   ├── .env.example                 # Template config
│   └── .gitignore                   # Archivos ignorados
│
├── 🚀 Setup & Automation
│   ├── setup.sh                     # Instalación Linux/Mac
│   └── setup.bat                    # Instalación Windows
│
├── 📚 Documentación
│   ├── README.md                    # ⭐ Inicio
│   ├── GUIA_RAPIDA.md              # Quick start
│   ├── README_MARKETPLACE_SCRAPER.md  # Docs técnicas
│   ├── COMO_AGREGAR_FACTURAS.md    # Guía facturas
│   └── ARQUITECTURA.md              # Este archivo
│
└── 📊 Output (Generados)
    ├── marketplace_products.json     # ⭐ Productos scrapeados
    └── marketplace_products_web.json # Formato web
```

---

## 🔐 Seguridad y Privacidad

### Variables de Entorno (.env)
```
.env (NO subir a GitHub)
  │
  ├─→ FACEBOOK_EMAIL=usuario@email.com
  ├─→ FACEBOOK_PASSWORD=contraseña_segura
  ├─→ GOOGLE_API_KEY=AIza...
  │
  └─→ Protegido por .gitignore
```

### .gitignore
```
.gitignore
  ├─→ .env                    # Credenciales
  ├─→ __pycache__/           # Python cache
  ├─→ venv/                  # Virtual environment
  ├─→ marketplace_products.json  # Output sensible
  └─→ *.log                  # Logs
```

---

## 🎯 Casos de Uso

### Caso 1: Scraping de Zapatillas
```
1. Configurar SEARCH_NICHE=zapatillas
2. Ejecutar scraper
3. Obtener 10 productos con:
   - Marca y modelo
   - Precio
   - Estado (nuevo/usado)
   - Fotos
   - Ubicación del vendedor
4. Integrar en página web
```

### Caso 2: Análisis de Precios
```
1. Scraper extrae precios de múltiples productos
2. IA estructura datos consistentemente
3. Exportar a JSON para análisis
4. Comparar precios entre vendedores
```

### Caso 3: Catálogo de Productos
```
1. Scraper recolecta productos diariamente
2. Acumular en base de datos
3. Mostrar en página web
4. Actualizar automáticamente
```

---

## 🔧 Personalización

### Cambiar Nicho de Búsqueda
```python
# En .env
SEARCH_NICHE=laptops        # Para laptops
SEARCH_NICHE=muebles        # Para muebles
SEARCH_NICHE=celulares      # Para celulares
```

### Ajustar Cantidad de Productos
```python
# En .env
MAX_PRODUCTS=20             # Más productos (más tiempo)
MAX_PRODUCTS=5              # Menos productos (más rápido)
```

### Modificar Prompt de IA
```python
# En marketplace_scraper.py, línea ~75
self.prompt = ChatPromptTemplate.from_messages([
    ("system", """
    TU PROMPT PERSONALIZADO AQUÍ
    Puedes ajustar cómo la IA extrae información
    """),
    ("user", "Extract product info from: {html_content}")
])
```

---

## 📈 Rendimiento

### Tiempos Estimados
```
Login a Facebook:      ~5 segundos
Búsqueda en Marketplace: ~3 segundos
Por producto:          ~5 segundos
  └─→ Carga página:    2s
  └─→ Análisis IA:     2s
  └─→ Delay:           1s

Total para 10 productos: ~1 minuto
```

### Costos API
```
Google GenAI (Gemini 1.5 Flash):
  • Tier gratuito: 15 requests/minuto
  • ~10 productos = 10 requests
  • Costo: Prácticamente $0 en tier gratuito
```

---

## 🐛 Debugging

### Logs del Scraper
```
✓ Login successful
✓ Marketplace loaded
  Found product: https://facebook.com/...
  Found product: https://facebook.com/...
✓ Found 10 product links

[1/10]
→ Scraping: https://facebook.com/...
  Warning: Failed to extract images: ...
✓ Product scraped: Nike Air Max 2024

[2/10]
...
```

### Verificar HTML Extraído
```python
# Los productos incluyen html_content
product.html_content  # Primeros 5000 caracteres

# Para debug completo, modificar marketplace_scraper.py:
html_content = page.content()  # HTML completo (sin límite)
```

---

## 🚀 Próximos Pasos

### Mejoras Futuras
- [ ] Scraping programado (cron jobs)
- [ ] Base de datos para almacenar productos
- [ ] API REST para servir productos
- [ ] Dashboard de analytics
- [ ] Notificaciones de nuevos productos
- [ ] Comparación de precios históricos
- [ ] Sistema de alertas por precio
- [ ] Integración con Telegram/WhatsApp

---

## 📞 Recursos

- [Playwright Docs](https://playwright.dev/python/)
- [LangChain Docs](https://python.langchain.com/)
- [Google AI Studio](https://makersuite.google.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

**Sistema diseñado para ser modular, escalable y fácil de mantener** ✨

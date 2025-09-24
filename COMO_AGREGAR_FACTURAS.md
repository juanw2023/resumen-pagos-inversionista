# 📋 Cómo Agregar Nuevas Facturas al Sistema

## 🎯 Resumen
Para agregar una nueva factura al sistema, necesitas modificar **DOS lugares principales**:
1. **HTML**: Agregar la tarjeta visual
2. **JSON**: Agregar los datos del modal

---

## 📝 PASO 1: Agregar la Tarjeta HTML

### Ubicación
En el archivo `index.html`, busca la sección `<section class="grid">` donde están las demás tarjetas.

### Estructura de la Tarjeta
```html
<article class="card" data-id="ID_UNICO" data-name="Nombre del Servicio" data-amount="MONTO" data-currency="USD_O_PEN">
    <div class="row">
        <h3>Título del Servicio</h3>
        <span class="space"></span>
        <span class="pill ESTADO">Estado</span>
    </div>
    <p class="amount">$MONTO MONEDA</p>
    <p class="meta">Descripción del servicio y detalles adicionales.</p>
    <div class="row" style="margin-top:16px;">
        <button class="btn btn-primary add-to-cart-btn">
            <svg class="icon"><use href="#icon-cart"></use></svg>
            <span>Añadir al Carrito</span>
        </button>
        <button class="btn btn-secondary view-detail-btn">
            <svg class="icon"><use href="#icon-eye"></use></svg>
            <span>Ver Detalle</span>
        </button>
    </div>
</article>
```

### Parámetros Importantes:
- **`data-id`**: ID único (ejemplo: "nueva-factura-001")
- **`data-name`**: Nombre que aparecerá en el carrito
- **`data-amount`**: Monto numérico (sin símbolos)
- **`data-currency`**: "USD" o "PEN"
- **Estado (pill)**: "danger" (rojo), "warn" (amarillo), "ok" (verde)

### Ejemplo Real:
```html
<article class="card" data-id="aws-hosting" data-name="Amazon AWS Hosting" data-amount="89.50" data-currency="USD">
    <div class="row">
        <h3>Amazon AWS Hosting</h3>
        <span class="space"></span>
        <span class="pill warn">Por Vencer</span>
    </div>
    <p class="amount">$89.50 USD</p>
    <p class="meta">Hosting en la nube de Amazon Web Services para nuestros proyectos principales. Incluye EC2, S3 y CloudFront.</p>
    <div class="row" style="margin-top:16px;">
        <button class="btn btn-primary add-to-cart-btn">
            <svg class="icon"><use href="#icon-cart"></use></svg>
            <span>Añadir al Carrito</span>
        </button>
        <button class="btn btn-secondary view-detail-btn">
            <svg class="icon"><use href="#icon-eye"></use></svg>
            <span>Ver Detalle</span>
        </button>
    </div>
</article>
```

---

## 📊 PASO 2: Agregar Datos del Modal (JSON)

### Ubicación
En el archivo `index.html`, busca la sección `"detalles_facturas": {` dentro del script JSON embebido.

### Estructura del JSON
```json
"ID_UNICO": {
    "nombre": "Nombre del Servicio",
    "descripcion": "Descripción detallada del servicio y la factura. Monto: $XX.XX",
    "screenshot": "assets/nombre_factura.png",
    "factura_pdf": "assets/nombre_factura.pdf"
}
```

### Ejemplo Real:
```json
"aws-hosting": {
    "nombre": "Amazon AWS Hosting",
    "descripcion": "Servicios de hosting en la nube de Amazon Web Services. Incluye instancias EC2, almacenamiento S3 y distribución CloudFront. Importe: $89.50",
    "screenshot": "assets/aws_factura.png",
    "factura_pdf": "assets/AWSFE001-112024-09-2025.pdf"
}
```

---

## 📁 PASO 3: Agregar Archivos de Documentos

### Ubicación de Archivos
Coloca los archivos en la carpeta `assets/`:
- **Imágenes**: `.png`, `.jpg`, `.jpeg`
- **PDFs**: `.pdf`

### Nombres Recomendados:
- **Screenshots**: `nombre_servicio_factura.png`
- **PDFs**: `EMPRESAFE001-DDMMAA-MM-AAAA.pdf`

### Ejemplos:
```
assets/
├── aws_factura.png
├── AWSFE001-112024-09-2025.pdf
├── netflix_factura.png
└── NETFLIXFE001-112024-09-2025.pdf
```

---

## 💡 CONSEJOS Y MEJORES PRÁCTICAS

### ✅ DO's (Hacer):
- Usa IDs únicos y descriptivos
- Mantén consistencia en los nombres
- Agrega descripciones claras y útiles
- Usa montos sin símbolos en `data-amount`
- Coloca archivos en `assets/` con nombres descriptivos

### ❌ DON'Ts (No hacer):
- No uses espacios en los IDs (usa guiones: `-`)
- No olvides agregar tanto HTML como JSON
- No uses caracteres especiales en nombres de archivo
- No olvides especificar la moneda correcta

### 🔧 Después de Agregar:
1. **Prueba la tarjeta**: Verifica que se vea correctamente
2. **Prueba "Añadir al Carrito"**: Confirma que funciona
3. **Prueba "Ver Detalle"**: Verifica que se abra el modal
4. **Prueba archivos**: Confirma que las imágenes y PDFs se cargan

---

## 🚀 Ejemplo Completo: Agregando Netflix

### 1. HTML (en la sección grid):
```html
<article class="card" data-id="netflix-premium" data-name="Netflix Premium" data-amount="45.90" data-currency="PEN">
    <div class="row">
        <h3>Netflix Premium</h3>
        <span class="space"></span>
        <span class="pill ok">Activo</span>
    </div>
    <p class="amount">S/ 45.90 PEN</p>
    <p class="meta">Suscripción mensual a Netflix Premium con 4 pantallas simultáneas y contenido 4K.</p>
    <div class="row" style="margin-top:16px;">
        <button class="btn btn-primary add-to-cart-btn">
            <svg class="icon"><use href="#icon-cart"></use></svg>
            <span>Añadir al Carrito</span>
        </button>
        <button class="btn btn-secondary view-detail-btn">
            <svg class="icon"><use href="#icon-eye"></use></svg>
            <span>Ver Detalle</span>
        </button>
    </div>
</article>
```

### 2. JSON (en detalles_facturas):
```json
"netflix-premium": {
    "nombre": "Netflix Premium",
    "descripcion": "Suscripción mensual a Netflix Premium con acceso a 4 pantallas simultáneas y contenido en 4K. Importe: S/ 45.90",
    "screenshot": "assets/netflix_factura.png",
    "factura_pdf": "assets/NETFLIXFE001-152024-09-2025.pdf"
}
```

### 3. Archivos:
- `assets/netflix_factura.png`
- `assets/NETFLIXFE001-152024-09-2025.pdf`

---

¡Y listo! Tu nueva factura aparecerá en el sistema con funcionalidad completa. 🎉

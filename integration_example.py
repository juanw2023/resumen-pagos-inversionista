"""
Example script to integrate marketplace products with the existing invoice system
This demonstrates how to format scraped products for display on the webpage
"""

import json
from typing import List, Dict


def load_marketplace_products(filename: str = "marketplace_products.json") -> Dict:
    """Load marketplace products from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run marketplace_scraper.py first.")
        return {"products": []}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}")
        return {"products": []}


def generate_product_html(product: Dict) -> str:
    """
    Generate HTML card for a product (similar to invoice cards)
    
    Args:
        product: Product dictionary with all details
        
    Returns:
        HTML string for the product card
    """
    # Extract product data with defaults
    product_id = product.get('url', '').split('/')[-1] or 'unknown'
    title = product.get('title', 'Product')
    price = product.get('price', 'Price not available')
    location = product.get('location', '')
    description = product.get('description', 'No description available')
    condition = product.get('condition', '')
    images = product.get('images', [])
    url = product.get('url', '#')
    
    # Get first image if available
    image_url = images[0].get('url') if images else None
    
    # Create status badge based on condition
    status_class = 'ok' if condition and 'new' in condition.lower() else 'warn'
    status_text = condition or 'Usado'
    
    html = f"""
    <article class="card marketplace-product" data-id="{product_id}" data-name="{title}">
        <div class="row">
            <h3>{title}</h3>
            <span class="space"></span>
            <span class="pill {status_class}">{status_text}</span>
        </div>
        <p class="amount">{price}</p>
        <p class="meta">{description[:150]}{'...' if len(description) > 150 else ''}</p>
        {f'<p class="meta" style="font-size: 0.9em; color: var(--text-muted);">📍 {location}</p>' if location else ''}
        
        <div class="row" style="margin-top:16px;">
            <button class="btn btn-primary" onclick="window.open('{url}', '_blank')">
                <svg class="icon" width="16" height="16"><use href="#icon-eye"></use></svg>
                <span>Ver en Marketplace</span>
            </button>
            <button class="btn btn-secondary view-product-detail-btn" data-product-id="{product_id}">
                <svg class="icon" width="16" height="16"><use href="#icon-eye"></use></svg>
                <span>Ver Detalle</span>
            </button>
        </div>
    </article>
    """
    
    return html


def generate_product_detail_json(product: Dict) -> Dict:
    """
    Generate product detail object for modal (similar to detalles_facturas)
    
    Args:
        product: Product dictionary
        
    Returns:
        Dictionary with product details for modal
    """
    product_id = product.get('url', '').split('/')[-1] or 'unknown'
    images = product.get('images', [])
    
    detail = {
        "nombre": product.get('title', 'Product'),
        "descripcion": f"{product.get('description', 'No description')} | Condición: {product.get('condition', 'N/A')} | Ubicación: {product.get('location', 'N/A')}",
        "screenshot": images[0].get('url') if images else None,
        "factura_pdf": None,  # Marketplace products don't have PDFs
        "product_url": product.get('url', '#'),
        "price": product.get('price', 'N/A'),
        "condition": product.get('condition', 'N/A'),
        "location": product.get('location', 'N/A'),
        "seller_info": product.get('seller_info', 'N/A'),
        "images": [img.get('url') for img in images]
    }
    
    return {product_id: detail}


def convert_to_webpage_format(input_file: str = "marketplace_products.json", 
                               output_file: str = "marketplace_products_web.json"):
    """
    Convert scraped marketplace products to format ready for webpage integration
    
    Args:
        input_file: Input JSON file with scraped products
        output_file: Output JSON file formatted for web
    """
    # Load products
    data = load_marketplace_products(input_file)
    products = data.get('products', [])
    
    if not products:
        print("No products found to convert.")
        return
    
    # Generate HTML for all products
    html_cards = []
    product_details = {}
    
    for product in products:
        html_cards.append(generate_product_html(product))
        product_details.update(generate_product_detail_json(product))
    
    # Create output data
    output = {
        "metadata": {
            "niche": data.get('niche', 'unknown'),
            "total_products": len(products),
            "timestamp": data.get('timestamp', '')
        },
        "html_cards": html_cards,
        "product_details": product_details
    }
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Converted {len(products)} products")
    print(f"✓ Output saved to: {output_file}")
    
    # Print sample HTML
    print("\n" + "="*60)
    print("SAMPLE HTML (add to index.html in the grid section):")
    print("="*60)
    if html_cards:
        print(html_cards[0])
    
    print("\n" + "="*60)
    print("SAMPLE DETAIL JSON (add to detalles_facturas object):")
    print("="*60)
    if product_details:
        first_key = list(product_details.keys())[0]
        print(json.dumps({first_key: product_details[first_key]}, indent=2, ensure_ascii=False))


def generate_integration_instructions():
    """Print instructions for integrating with the existing webpage"""
    instructions = """
    
╔══════════════════════════════════════════════════════════════════════════════╗
║                    INTEGRATION INSTRUCTIONS                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 Steps to integrate marketplace products with your webpage:

1️⃣  RUN THE SCRAPER
   python marketplace_scraper.py
   
2️⃣  CONVERT TO WEB FORMAT
   python integration_example.py
   
3️⃣  INTEGRATE HTML CARDS
   Open index.html and add the HTML cards from marketplace_products_web.json
   to the <section class="grid"> section (around line 1300)
   
4️⃣  ADD PRODUCT DETAILS
   Add the product_details JSON to the "detalles_facturas" object in index.html
   (around line 1550)
   
5️⃣  UPDATE JAVASCRIPT (Optional)
   Add product modal handling to the existing JavaScript:
   
   document.querySelectorAll('.view-product-detail-btn').forEach(btn => {
       btn.addEventListener('click', function() {
           const productId = this.dataset.productId;
           // Show product modal similar to invoice detail modal
       });
   });

📝 EXAMPLE INTEGRATION:

In index.html, after the existing service cards:

<!-- Marketplace Products Section -->
<h2 class="section-title" style="margin-top: 40px;">🛒 Productos de Marketplace</h2>
<section class="grid">
    <!-- Paste HTML cards here -->
</section>

✨ The products will automatically match your existing dark theme and styling!

═══════════════════════════════════════════════════════════════════════════════
    """
    print(instructions)


if __name__ == "__main__":
    print("="*60)
    print("Marketplace Products Integration Tool")
    print("="*60)
    
    # Convert products to web format
    convert_to_webpage_format()
    
    # Show integration instructions
    generate_integration_instructions()

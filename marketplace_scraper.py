"""
Facebook Marketplace Scraper with LangChain and Google GenAI
Extracts product information from Facebook Marketplace and structures it using AI
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

# Load environment variables
load_dotenv()

# Define constants
NICHE = "zapatillas"  # Product niche to search for
MAX_PRODUCTS = 10  # Maximum number of products to scrape


class ProductImage(BaseModel):
    """Product image information"""
    url: str = Field(description="Image URL")
    alt_text: Optional[str] = Field(default=None, description="Alternative text for image")


class Product(BaseModel):
    """Structured product information"""
    title: str = Field(description="Product title/name")
    price: str = Field(description="Product price with currency")
    location: Optional[str] = Field(default=None, description="Seller location")
    description: Optional[str] = Field(default=None, description="Product description")
    condition: Optional[str] = Field(default=None, description="Product condition (new, used, etc)")
    images: List[ProductImage] = Field(default_factory=list, description="List of product images")
    url: str = Field(description="Product URL")
    seller_info: Optional[str] = Field(default=None, description="Seller information")
    html_content: Optional[str] = Field(default=None, description="Raw HTML content of the product")


class MarketplaceScraper:
    """Facebook Marketplace scraper with AI-powered data extraction"""
    
    def __init__(self, email: str, password: str, niche: str = NICHE):
        """
        Initialize the scraper
        
        Args:
            email: Facebook account email
            password: Facebook account password
            niche: Product niche to search for
        """
        self.email = email
        self.password = password
        self.niche = niche
        self.products = []
        
        # Initialize LangChain with Google GenAI
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.3
        )
        
        # Setup output parser
        self.parser = PydanticOutputParser(pydantic_object=Product)
        
        # Create prompt template for AI analysis
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at extracting structured product information from HTML content.
            Extract all relevant product details including title, price, location, description, condition, and images.
            Be thorough and accurate. If information is not available, use null.
            
            {format_instructions}
            """),
            ("user", "Extract product information from this HTML:\n\n{html_content}")
        ])

    def login_to_facebook(self, page):
        """
        Logs in to Facebook
        
        Args:
            page: Playwright page object
        """
        try:
            page.goto("https://www.facebook.com/", timeout=60000)
            time.sleep(2)
            
            # Try different placeholder variations
            try:
                page.get_by_placeholder("Email or phone number").fill(self.email)
            except:
                try:
                    page.get_by_placeholder("Correo electrónico o número de teléfono").fill(self.email)
                except:
                    page.locator('input[name="email"]').fill(self.email)
            
            try:
                page.get_by_placeholder("Password").fill(self.password)
            except:
                try:
                    page.get_by_placeholder("Contraseña").fill(self.password)
                except:
                    page.locator('input[name="pass"]').fill(self.password)
            
            # Click login button
            try:
                page.get_by_role("button", name="Log In").click()
            except:
                try:
                    page.get_by_role("button", name="Iniciar sesión").click()
                except:
                    page.locator('button[name="login"]').click()
            
            # Wait for login to complete
            page.wait_for_load_state("networkidle", timeout=60000)
            time.sleep(3)
            print("✓ Login successful")
            
        except Exception as e:
            print(f"✗ Login failed: {e}")
            raise

    def navigate_to_marketplace(self, page):
        """
        Navigate to Facebook Marketplace and search for products
        
        Args:
            page: Playwright page object
        """
        try:
            # Go to Marketplace
            print(f"Navigating to Marketplace for: {self.niche}")
            marketplace_url = f"https://www.facebook.com/marketplace/search/?query={self.niche}"
            page.goto(marketplace_url, timeout=60000)
            time.sleep(5)
            
            # Wait for products to load
            page.wait_for_selector('div[role="main"]', timeout=30000)
            time.sleep(3)
            print("✓ Marketplace loaded")
            
        except Exception as e:
            print(f"✗ Failed to navigate to Marketplace: {e}")
            raise

    def extract_product_links(self, page, max_products=MAX_PRODUCTS):
        """
        Extract product links from the marketplace search results
        
        Args:
            page: Playwright page object
            max_products: Maximum number of product links to extract
            
        Returns:
            List of product URLs
        """
        product_links = []
        
        try:
            # Scroll to load more products
            for _ in range(3):
                page.evaluate("window.scrollBy(0, window.innerHeight)")
                time.sleep(2)
            
            # Find all product links
            links = page.locator('a[href*="/marketplace/item/"]').all()
            
            for link in links[:max_products]:
                try:
                    href = link.get_attribute('href')
                    if href and '/marketplace/item/' in href:
                        full_url = href if href.startswith('http') else f"https://www.facebook.com{href}"
                        if full_url not in product_links:
                            product_links.append(full_url)
                            print(f"  Found product: {full_url}")
                except:
                    continue
            
            print(f"✓ Found {len(product_links)} product links")
            return product_links[:max_products]
            
        except Exception as e:
            print(f"✗ Failed to extract product links: {e}")
            return product_links

    def scrape_product_page(self, page, product_url):
        """
        Scrape individual product page
        
        Args:
            page: Playwright page object
            product_url: URL of the product to scrape
            
        Returns:
            Raw HTML content and extracted data
        """
        try:
            print(f"\n→ Scraping: {product_url}")
            page.goto(product_url, timeout=60000)
            time.sleep(3)
            
            # Wait for product content to load
            page.wait_for_selector('div[role="main"]', timeout=30000)
            time.sleep(2)
            
            # Get the full HTML of the product page
            html_content = page.content()
            
            # Extract images
            images = []
            try:
                img_elements = page.locator('img').all()
                for img in img_elements[:5]:  # Limit to first 5 images
                    try:
                        src = img.get_attribute('src')
                        alt = img.get_attribute('alt') or ""
                        if src and ('scontent' in src or 'fbcdn' in src):
                            images.append({
                                'url': src,
                                'alt_text': alt
                            })
                    except:
                        continue
            except Exception as e:
                print(f"  Warning: Failed to extract images: {e}")
            
            # Extract basic information directly (as backup)
            basic_info = {
                'url': product_url,
                'images': images,
                'html_content': html_content[:5000]  # Limit HTML size
            }
            
            return html_content, basic_info
            
        except Exception as e:
            print(f"✗ Failed to scrape product page: {e}")
            return None, None

    def analyze_with_ai(self, html_content, basic_info):
        """
        Use LangChain and Google GenAI to analyze and structure product data
        
        Args:
            html_content: Raw HTML content
            basic_info: Basic extracted information
            
        Returns:
            Structured Product object
        """
        try:
            # Prepare the prompt with format instructions
            format_instructions = self.parser.get_format_instructions()
            
            # Limit HTML content to avoid token limits
            html_snippet = html_content[:8000] if html_content else ""
            
            # Create the chain
            chain = self.prompt | self.llm
            
            # Run the chain
            result = chain.invoke({
                "html_content": html_snippet,
                "format_instructions": format_instructions
            })
            
            # Parse the result
            try:
                product = self.parser.parse(result.content)
                
                # Merge with basic info (images, URL)
                if not product.images and basic_info.get('images'):
                    product.images = [ProductImage(**img) for img in basic_info['images']]
                if not product.url:
                    product.url = basic_info.get('url', '')
                if not product.html_content:
                    product.html_content = basic_info.get('html_content', '')
                
                return product
                
            except Exception as parse_error:
                print(f"  Warning: Failed to parse AI response, using basic info: {parse_error}")
                # Fallback: create product from basic info
                return self.create_fallback_product(basic_info)
            
        except Exception as e:
            print(f"  Warning: AI analysis failed, using basic info: {e}")
            return self.create_fallback_product(basic_info)

    def create_fallback_product(self, basic_info):
        """
        Create a basic Product object from scraped data when AI parsing fails
        
        Args:
            basic_info: Basic extracted information
            
        Returns:
            Product object
        """
        return Product(
            title="Product information extracted",
            price="See listing",
            url=basic_info.get('url', ''),
            images=[ProductImage(**img) for img in basic_info.get('images', [])],
            html_content=basic_info.get('html_content', '')
        )

    def scrape_marketplace(self, max_products=MAX_PRODUCTS):
        """
        Main method to scrape Facebook Marketplace
        
        Args:
            max_products: Maximum number of products to scrape
            
        Returns:
            List of structured Product objects
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=100)
            page = browser.new_page()
            page.set_viewport_size({"width": 1920, "height": 1080})
            
            try:
                # Login to Facebook
                self.login_to_facebook(page)
                
                # Navigate to Marketplace
                self.navigate_to_marketplace(page)
                
                # Extract product links
                product_links = self.extract_product_links(page, max_products)
                
                # Scrape each product
                for i, product_url in enumerate(product_links, 1):
                    print(f"\n[{i}/{len(product_links)}]")
                    
                    html_content, basic_info = self.scrape_product_page(page, product_url)
                    
                    if html_content and basic_info:
                        # Analyze with AI
                        product = self.analyze_with_ai(html_content, basic_info)
                        
                        if product:
                            self.products.append(product)
                            print(f"✓ Product scraped: {product.title}")
                    
                    # Delay between requests
                    time.sleep(3)
                
                print(f"\n✓ Scraping complete! Total products: {len(self.products)}")
                
            except Exception as e:
                print(f"\n✗ Scraping failed: {e}")
                
            finally:
                browser.close()
        
        return self.products

    def save_to_json(self, filename="marketplace_products.json"):
        """
        Save scraped products to JSON file
        
        Args:
            filename: Output filename
        """
        try:
            output_data = {
                "niche": self.niche,
                "total_products": len(self.products),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "products": [product.dict() for product in self.products]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Data saved to {filename}")
            return filename
            
        except Exception as e:
            print(f"✗ Failed to save JSON: {e}")
            return None


def main():
    """Main function to run the scraper"""
    # Get credentials from environment
    email = os.getenv("FACEBOOK_EMAIL")
    password = os.getenv("FACEBOOK_PASSWORD")
    
    if not email or not password:
        print("Error: FACEBOOK_EMAIL and FACEBOOK_PASSWORD must be set in .env file")
        return
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY must be set in .env file")
        return
    
    # Get optional parameters
    niche = os.getenv("SEARCH_NICHE", NICHE)
    max_products = int(os.getenv("MAX_PRODUCTS", MAX_PRODUCTS))
    
    print("=" * 60)
    print("Facebook Marketplace Scraper with AI")
    print("=" * 60)
    print(f"Niche: {niche}")
    print(f"Max products: {max_products}")
    print("=" * 60 + "\n")
    
    # Create scraper and run
    scraper = MarketplaceScraper(email, password, niche)
    products = scraper.scrape_marketplace(max_products)
    
    # Save results
    if products:
        output_file = scraper.save_to_json()
        print(f"\n{'=' * 60}")
        print(f"Scraping complete!")
        print(f"Products scraped: {len(products)}")
        print(f"Output file: {output_file}")
        print(f"{'=' * 60}")
    else:
        print("\nNo products were scraped.")


if __name__ == "__main__":
    main()

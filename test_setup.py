"""
Test script to verify marketplace scraper setup and dependencies
Run this before attempting to scrape Facebook Marketplace
"""

import sys
import os


def test_python_version():
    """Check Python version"""
    print("Testing Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (requires 3.8+)")
        return False


def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    display_name = package_name or module_name
    print(f"Testing {display_name}...", end=" ")
    try:
        __import__(module_name)
        print("✓")
        return True
    except ImportError as e:
        print(f"✗ ({e})")
        return False


def test_environment_variables():
    """Check if required environment variables are set"""
    print("\nTesting environment variables:")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        "FACEBOOK_EMAIL": "Facebook email address",
        "FACEBOOK_PASSWORD": "Facebook password",
        "GOOGLE_API_KEY": "Google API key for GenAI"
    }
    
    all_set = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Show partial value for security
            display_value = value[:10] + "..." if len(value) > 10 else value[:5] + "..."
            print(f"  ✓ {var}: {display_value}")
        else:
            print(f"  ✗ {var}: Not set ({description})")
            all_set = False
    
    return all_set


def test_playwright_installation():
    """Check if Playwright browsers are installed"""
    print("\nTesting Playwright browser installation...", end=" ")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Try to launch chromium
            browser = p.chromium.launch(headless=True)
            browser.close()
        print("✓ Chromium browser installed")
        return True
    except Exception as e:
        print(f"✗ Browser not installed or error: {e}")
        print("  Run: playwright install chromium")
        return False


def test_langchain_setup():
    """Test LangChain and Google GenAI setup"""
    print("\nTesting LangChain and Google GenAI setup...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("  ✗ GOOGLE_API_KEY not set")
            return False
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        print("  Testing API connection...", end=" ")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.3
        )
        
        # Try a simple test
        result = llm.invoke("Say 'test' in one word")
        print("✓ API connection successful")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("="*70)
    print("Marketplace Scraper - System Check")
    print("="*70 + "\n")
    
    results = []
    
    # Test Python version
    results.append(("Python Version", test_python_version()))
    
    print("\nTesting Python dependencies:")
    print("-" * 70)
    
    # Test imports
    dependencies = [
        ("playwright.sync_api", "Playwright"),
        ("dotenv", "python-dotenv"),
        ("langchain", "LangChain"),
        ("langchain_google_genai", "LangChain Google GenAI"),
        ("google.generativeai", "Google GenerativeAI"),
        ("pydantic", "Pydantic"),
    ]
    
    for module, display_name in dependencies:
        results.append((display_name, test_import(module, display_name)))
    
    # Test environment variables
    print("\n" + "-" * 70)
    results.append(("Environment Variables", test_environment_variables()))
    
    # Test Playwright
    print("\n" + "-" * 70)
    results.append(("Playwright Browsers", test_playwright_installation()))
    
    # Test LangChain + GenAI
    print("\n" + "-" * 70)
    results.append(("LangChain + GenAI", test_langchain_setup()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:10} | {name}")
    
    print("-" * 70)
    print(f"TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! You're ready to run the scraper.")
        print("\nRun: python marketplace_scraper.py")
    else:
        print("\n✗ Some tests failed. Please fix the issues above before running the scraper.")
        print("\nQuick fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Install Playwright browsers: playwright install chromium")
        print("  3. Configure .env file: cp .env.example .env (then edit with your credentials)")
    
    print("="*70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

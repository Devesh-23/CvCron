from playwright.sync_api import sync_playwright
import os

def launch_browser(headless=True, user_agent=None):
    # Force headless in production/server environment
    if os.getenv('RENDER') or os.getenv('PORT'):
        headless = True
    """
    Launch browser and return playwright instance, browser, and page
    
    Args:
        headless (bool): Whether to run in headless mode
        user_agent (str): Custom user agent string
        
    Returns:
        tuple: (playwright_instance, browser, page)
    """
    pw = sync_playwright().start()
    
    # Browser launch arguments for better compatibility
    browser_args = [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-blink-features=AutomationControlled',
        '--disable-web-security',
        '--disable-features=VizDisplayCompositor'
    ]
    
    browser = pw.chromium.launch(
        headless=headless,
        args=browser_args
    )
    
    # Create context with realistic settings
    context = browser.new_context(
        viewport={'width': 1366, 'height': 768},
        user_agent=user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    )
    
    # Create page
    page = context.new_page()
    
    # Add some stealth settings
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        window.chrome = {
            runtime: {}
        };
        
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
    """)
    
    return pw, browser, page
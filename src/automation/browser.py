from playwright.sync_api import sync_playwright
import os

def launch_browser(headless=True, user_agent=None):
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
    
    # Don't force headless in CI - use Xvfb virtual display instead
    # This avoids Naukri's headless browser detection
    
    # Add proxy if in CI environment
    launch_options = {
        'headless': headless,
        'args': browser_args
    }
    
    # Use proxy in CI to avoid IP blocks
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
        # Free proxy services (rotate these)
        proxies = [
            'socks5://proxy.example.com:1080',  # Replace with actual proxy
            # Add more proxy servers here
        ]
        # Uncomment and add real proxy if available
        # launch_options['proxy'] = {'server': proxies[0]}
    
    browser = pw.chromium.launch(**launch_options)
    
    # Use different user agent in CI to avoid detection
    default_ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
        # More generic user agent for CI
        default_ua = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    # Create context with realistic settings and stealth headers
    context = browser.new_context(
        viewport={'width': 1366, 'height': 768},
        user_agent=user_agent or default_ua,
        extra_http_headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
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
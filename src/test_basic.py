import os
from .config_loader import load_config, load_env
from .automation.browser import launch_browser
from .logger import get_logger

log = get_logger(__name__)

def wait_and_screenshot(page, filename="debug.png", delay=2):
    """Wait a bit and take screenshot for debugging"""
    import time
    time.sleep(delay)
    try:
        os.makedirs("logs", exist_ok=True)
        page.screenshot(path=f"logs/{filename}", full_page=True)
        log.info(f"Screenshot saved: logs/{filename}")
    except Exception as e:
        log.warning(f"Could not save screenshot: {e}")

def test_naukri_access():
    """Test basic access to Naukri and take screenshots for inspection"""
    try:
        cfg = load_config()
        creds = load_env()
        
        log.info("Starting Naukri access test...")
        
        # Launch browser in non-headless mode for initial testing
        pw, browser, context, page = launch_browser(headless=False)
        
        try:
            # Go to Naukri homepage first
            log.info("Navigating to Naukri.com...")
            page.goto("https://www.naukri.com", wait_until="domcontentloaded")
            wait_and_screenshot(page, "01_homepage.png")
            
            # Look for login link/button
            log.info("Looking for login options...")
            
            # Common login selectors to try
            login_selectors = [
                'a:has-text("Login")',
                'button:has-text("Login")', 
                '[data-ga-track*="Login"]',
                '.login',
                '#login',
                'text=Login'
            ]
            
            login_found = False
            for selector in login_selectors:
                try:
                    if page.is_visible(selector, timeout=2000):
                        log.info(f"Found login element: {selector}")
                        page.click(selector)
                        login_found = True
                        break
                except:
                    continue
            
            if not login_found:
                log.warning("No login button found, trying direct navigation to login page")
                page.goto("https://www.naukri.com/nlogin/login", wait_until="domcontentloaded")
            
            page.wait_for_timeout(3000)
            wait_and_screenshot(page, "02_login_page.png")
            
            # Try to identify login form elements
            log.info("Analyzing login form...")
            
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[name="emailId"]',
                'input[id="usernameField"]',
                'input[placeholder*="email"]',
                'input[placeholder*="Email"]'
            ]
            
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[id="passwordField"]',
                'input[placeholder*="password"]',
                'input[placeholder*="Password"]'
            ]
            
            # Check which selectors work
            found_email = False
            found_password = False
            
            for selector in email_selectors:
                try:
                    if page.is_visible(selector, timeout=2000):
                        log.info(f"✓ Found email input: {selector}")
                        found_email = True
                        break
                except:
                    continue
            
            for selector in password_selectors:
                try:
                    if page.is_visible(selector, timeout=2000):
                        log.info(f"✓ Found password input: {selector}")
                        found_password = True
                        break
                except:
                    continue
            
            if found_email and found_password:
                log.info("✓ Login form elements found successfully!")
            else:
                log.warning("⚠ Some login elements not found")
            
            log.info("Test completed. Check logs/ folder for screenshots.")
            log.info("Press Enter to close browser...")
            input()
            
        finally:
            context.close()
            browser.close()
            pw.stop()
            
    except Exception as e:
        log.exception(f"Test failed: {e}")

if __name__ == "__main__":
    test_naukri_access()
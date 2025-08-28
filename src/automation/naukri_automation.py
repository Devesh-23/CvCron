import time
import os
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from ..logger import get_logger
from .browser import launch_browser

class NaukriAutomation:
    def __init__(self, config, credentials):
        self.config = config
        self.credentials = credentials
        self.logger = get_logger("naukri_automation")
        self.browser = None
        self.page = None
        self.pw = None
        
    def setup_browser(self):
        """Initialize browser and page"""
        try:
            self.logger.info("Setting up browser...")
            headless = self.credentials.get("headless", True)
            user_agent = self.config.get("user_agent", "auto")
            
            self.pw, self.browser, self.page = launch_browser(
                headless=headless, 
                user_agent=user_agent if user_agent != "auto" else None
            )
            self.logger.info("Browser setup complete")
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup browser: {e}")
            return False
    
    def login(self):
        """Login to Naukri account"""
        try:
            self.logger.info("Starting login process...")
            
            # Navigate to Naukri login page
            self.page.goto("https://www.naukri.com/nlogin/login", wait_until="networkidle")
            time.sleep(3)
            
            # Take screenshot for debugging
            os.makedirs("logs", exist_ok=True)
            self.page.screenshot(path="logs/01_login_page.png")
            
            # Log page content for debugging
            with open("logs/login_page_content.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            
            self.logger.info(f"Current URL: {self.page.url}")
            self.logger.info(f"Page title: {self.page.title()}")
            
            # Try multiple email selectors
            email_selectors = [
                "#usernameField",
                "input[placeholder='Enter Email ID / Username']",
                "input[name='email']",
                "input[type='email']",
                "input[type='text']",
                "#emailId",
                "input[placeholder*='Email']",
                "input[placeholder*='email']",
                "input[placeholder*='Username']",
                "input[id*='email']",
                "input[class*='email']",
                "input[data-automation='email']"
            ]
            
            email_filled = False
            for email_selector in email_selectors:
                try:
                    self.page.wait_for_selector(email_selector, timeout=5000)
                    self.page.fill(email_selector, self.credentials["email"])
                    self.logger.info(f"Email filled using selector: {email_selector}")
                    email_filled = True
                    break
                except:
                    continue
            
            if not email_filled:
                self.logger.error("Could not find email input field")
                return False
            
            # Try multiple password selectors
            password_selectors = [
                "#passwordField",
                "input[placeholder='Enter Password']",
                "input[name='password']",
                "input[type='password']",
                "#password",
                "input[placeholder*='Password']",
                "input[placeholder*='password']",
                "input[id*='password']",
                "input[class*='password']",
                "input[data-automation='password']"
            ]
            
            password_filled = False
            for password_selector in password_selectors:
                try:
                    self.page.wait_for_selector(password_selector, timeout=5000)
                    self.page.fill(password_selector, self.credentials["password"])
                    self.logger.info(f"Password filled using selector: {password_selector}")
                    password_filled = True
                    break
                except:
                    continue
            
            if not password_filled:
                self.logger.error("Could not find password input field")
                return False
            
            # Try to submit the form directly
            try:
                # Look for login button and click it
                login_button_selectors = [
                    "button[type='submit']:has-text('Login')",
                    "button:has-text('Login')",
                    ".btn:has-text('Login')",
                    "#loginForm button[type='submit']",
                    "input[type='submit']"
                ]
                
                button_clicked = False
                for button_selector in login_button_selectors:
                    try:
                        if self.page.locator(button_selector).count() > 0:
                            self.page.click(button_selector)
                            self.logger.info(f"Login button clicked: {button_selector}")
                            button_clicked = True
                            break
                    except:
                        continue
                
                if not button_clicked:
                    # Fallback to Enter key
                    self.page.focus("#passwordField")
                    self.page.keyboard.press("Enter")
                    self.logger.info("Form submitted using Enter key")
                
            except Exception as e:
                self.logger.error(f"Form submission failed: {e}")
                return False
            
            # Wait for login processing and handle any popups
            try:
                self.logger.info("Waiting for login to process...")
                time.sleep(5)
                
                # Handle any popup that might appear
                try:
                    popup_selectors = [
                        "button:has-text('Close')",
                        "button:has-text('Skip')",
                        "button:has-text('Later')",
                        "button:has-text('No Thanks')",
                        ".close",
                        ".modal-close",
                        "[data-dismiss='modal']",
                        ".popup-close",
                        "button[aria-label='Close']"
                    ]
                    
                    for popup_selector in popup_selectors:
                        try:
                            if self.page.locator(popup_selector).count() > 0:
                                self.page.click(popup_selector, timeout=2000)
                                self.logger.info(f"Closed popup using: {popup_selector}")
                                time.sleep(1)
                                break
                        except:
                            continue
                except Exception as e:
                    self.logger.info(f"No popup found or error closing popup: {e}")
                
                # Check current URL to see if login was successful
                current_url = self.page.url
                self.logger.info(f"Current URL after login: {current_url}")
                
                # If still on login page, login failed
                if "login" in current_url.lower():
                    self.logger.error("Login failed - still on login page")
                    self.page.screenshot(path="logs/02_login_failed.png")
                    return False
                
                # Try to navigate to profile page directly
                self.logger.info("Login successful, proceeding to profile")
                self.page.screenshot(path="logs/02_login_success.png")
                return True
                    
            except Exception as e:
                self.logger.error(f"Login process error: {e}")
                self.page.screenshot(path="logs/02_login_error.png")
                return False
                
        except Exception as e:
            self.logger.error(f"Login failed with error: {e}")
            if self.page:
                self.page.screenshot(path="logs/02_login_error.png")
            return False
    
    def navigate_to_profile(self):
        """Navigate to profile page where resume can be updated"""
        try:
            self.logger.info("Navigating to profile...")
            
            # Go directly to profile page
            profile_url = "https://www.naukri.com/mnjuser/profile"
            self.page.goto(profile_url, timeout=60000)
            time.sleep(3)
            
            self.logger.info("Profile page loaded")
            self.page.screenshot(path="logs/03_profile_page.png")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to profile: {e}")
            if self.page:
                self.page.screenshot(path="logs/03_profile_error.png")
            return False
    
    def upload_resume(self):
        """Upload or update resume"""
        try:
            self.logger.info("Starting resume upload...")
            
            resume_path = os.path.abspath(self.config["resume"]["path"])
            if not os.path.exists(resume_path):
                self.logger.error(f"Resume file not found: {resume_path}")
                return False
            
            # Look for file input directly (original working logic)
            possible_selectors = [
                "input[type='file'][accept*='pdf']",
                "input[type='file']",
                ".resume-upload input",
                ".upload-resume input",
                "button:has-text('Update Resume')",
                "button:has-text('Upload Resume')",
                ".resume-upload-btn",
                ".update-resume"
            ]
            
            resume_input = None
            upload_button = None
            
            # Try to find file input or upload button
            for selector in possible_selectors:
                try:
                    if "input[type='file']" in selector:
                        if self.page.locator(selector).count() > 0:
                            resume_input = selector
                            break
                    else:
                        if self.page.locator(selector).count() > 0:
                            upload_button = selector
                            break
                except:
                    continue
            
            # If we found an upload button, click it first
            if upload_button:
                self.logger.info(f"Clicking upload button: {upload_button}")
                self.page.click(upload_button)
                time.sleep(2)
                
                # Now look for file input again
                for selector in possible_selectors:
                    if "input[type='file']" in selector:
                        try:
                            if self.page.locator(selector).count() > 0:
                                resume_input = selector
                                break
                        except:
                            continue
            
            if resume_input:
                self.logger.info(f"Found file input: {resume_input}")
                self.page.set_input_files(resume_input, resume_path)
                self.logger.info("Resume file selected")
                
                # Wait for any processing
                time.sleep(self.config.get("behavior", {}).get("wait_after_upload_sec", 5))
                
                # Look for and click submit/save button if needed
                submit_selectors = [
                    "button:has-text('Save')",
                    "button:has-text('Update')",
                    "button:has-text('Upload')",
                    "button:has-text('Submit')",
                    ".save-btn",
                    ".submit-btn"
                ]
                
                for selector in submit_selectors:
                    try:
                        if self.page.locator(selector).count() > 0:
                            self.logger.info(f"Clicking submit button: {selector}")
                            self.page.click(selector)
                            time.sleep(3)
                            break
                    except:
                        continue
                
                self.logger.info("Resume upload completed")
                self.page.screenshot(path="logs/04_resume_uploaded.png")
                return True
            else:
                self.logger.error("Could not find resume upload input")
                self.page.screenshot(path="logs/04_upload_input_not_found.png")
                
                # Log page content for debugging
                with open("logs/page_content.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
                
                return False
                
        except Exception as e:
            self.logger.error(f"Resume upload failed: {e}")
            if self.page:
                self.page.screenshot(path="logs/04_upload_error.png")
            return False
    
    def run_automation(self):
        """Main automation flow"""
        try:
            self.logger.info("Starting Naukri automation...")
            
            # Setup browser
            if not self.setup_browser():
                return False
            
            # Login
            if not self.login():
                return False
            
            # Navigate to profile
            if not self.navigate_to_profile():
                return False
            
            # Upload resume
            if not self.upload_resume():
                return False
            
            self.logger.info("Automation completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Automation failed: {e}")
            return False
            
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.browser:
                self.browser.close()
            if self.pw:
                self.pw.stop()
            self.logger.info("Browser cleanup completed")
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")


# Main execution script
# File: src/run_automation.py

def main():
    """Main entry point for running the automation"""
    from .config_loader import load_config, load_env
    from .logger import get_logger
    
    logger = get_logger("main")
    
    try:
        # Load configuration
        config = load_config()
        credentials = load_env()
        
        # Validate credentials
        if not credentials["email"] or not credentials["password"]:
            logger.error("Email or password not set in .env file")
            return False
        
        # Run automation
        automation = NaukriAutomation(config, credentials)
        success = automation.run_automation()
        
        if success:
            logger.info("✅ Automation completed successfully!")
        else:
            logger.error("❌ Automation failed!")
            
        return success
        
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        return False

if __name__ == "__main__":
    main()
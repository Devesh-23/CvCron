import os

from .config_loader import load_config, load_env
from .logger import get_logger
from .automation.naukri_automation import NaukriAutomation

def main():
    """Test the Naukri automation"""
    logger = get_logger("test")
    
    try:
        logger.info("🚀 Starting Naukri automation test...")
        
        # Load configuration
        config = load_config()
        credentials = load_env()
        
        # Validate credentials
        if not credentials["email"] or not credentials["password"]:
            logger.error("❌ Email or password not set in .env file")
            logger.info("Please check your .env file and make sure NAUKRI_EMAIL and NAUKRI_PASSWORD are set")
            return False
        
        logger.info(f"📧 Using email: {credentials['email']}")
        logger.info(f"🔧 Headless mode: {credentials['headless']}")
        logger.info(f"📄 Resume path: {config['resume']['path']}")
        
        # Check if resume file exists
        if not os.path.exists(config['resume']['path']):
            logger.error(f"❌ Resume file not found: {config['resume']['path']}")
            logger.info("Please make sure your resume PDF is placed in the resumes/ folder")
            return False
        
        logger.info("✅ All prerequisites met, starting automation...")
        
        # Run automation
        automation = NaukriAutomation(config, credentials)
        success = automation.run_automation()
        
        if success:
            logger.info("🎉 Automation completed successfully!")
            logger.info("📸 Check the logs/ folder for screenshots")
        else:
            logger.error("💥 Automation failed!")
            logger.info("📸 Check the logs/ folder for error screenshots and details")
            
        return success
        
    except Exception as e:
        logger.error(f"💥 Test execution failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 NAUKRI RESUME AUTOMATION TEST")
    print("=" * 60)
    
    success = main()
    
    print("=" * 60)
    if success:
        print("✅ TEST COMPLETED SUCCESSFULLY!")
    else:
        print("❌ TEST FAILED - Check logs for details")
    print("=" * 60)
from flask import Flask, jsonify, request
import os
import logging
from src.automation.naukri_automation import NaukriAutomation
from src.config_loader import load_config, load_env

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "Naukri Resume Automation",
        "endpoints": {
            "/": "Service status",
            "/health": "Health check",
            "/update-resume": "Trigger resume update"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "naukri-automation"})

@app.route('/update-resume', methods=['POST', 'GET'])
def update_resume():
    try:
        logger.info("🚀 Resume update triggered")
        
        # Load configuration
        config = load_config()
        credentials = load_env()
        
        # Validate credentials
        if not credentials.get("email") or not credentials.get("password"):
            return jsonify({
                "success": False,
                "error": "Missing credentials"
            }), 400
        
        # Run automation
        automation = NaukriAutomation(config, credentials)
        success = automation.run_automation()
        
        if success:
            logger.info("✅ Resume update completed successfully")
            return jsonify({
                "success": True,
                "message": "Resume updated successfully on Naukri"
            })
        else:
            logger.error("❌ Resume update failed")
            return jsonify({
                "success": False,
                "error": "Automation failed - check logs"
            }), 500
            
    except Exception as e:
        logger.error(f"💥 Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
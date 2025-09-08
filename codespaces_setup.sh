#!/bin/bash

echo "🚀 Setting up Naukri Automation in Codespaces..."

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Set up environment variables (you'll need to add these manually)
echo "📝 Create .env file with your credentials:"
echo "NAUKRI_EMAIL=your_email@example.com"
echo "NAUKRI_PASSWORD=your_password"
echo "HEADLESS=true"

# Set up cron job for 5 AM IST (which is 11:30 PM UTC previous day)
CRON_COMMAND="30 23 * * * cd /workspaces/CvCron && python -m src.test_naukri >> logs/cron.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -

echo "✅ Setup complete!"
echo "📅 Cron job scheduled for 5:00 AM IST (11:30 PM UTC)"
echo "🔧 Don't forget to create .env file with your credentials"
echo "📊 Check logs with: tail -f logs/cron.log"
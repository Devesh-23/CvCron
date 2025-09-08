#!/bin/bash

# Get the current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Setting up cron job for Naukri Resume Automation..."
echo "Script directory: $SCRIPT_DIR"

# Create the cron job command
CRON_COMMAND="0 9 * * * cd $SCRIPT_DIR && source .venv/bin/activate && python -m src.test_naukri >> logs/cron.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -

echo "✅ Cron job added successfully!"
echo "📅 Schedule: Daily at 9:00 AM"
echo "📝 Logs will be saved to: $SCRIPT_DIR/logs/cron.log"
echo ""
echo "To view current cron jobs: crontab -l"
echo "To remove this cron job: crontab -e (then delete the line)"
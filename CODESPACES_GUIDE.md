# GitHub Codespaces Setup Guide

## Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Add Codespaces configuration"
git push origin main
```

## Step 2: Create Codespace
1. Go to your GitHub repository
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait for container to build (2-3 minutes)

## Step 3: Setup in Codespace
```bash
# Run setup script
chmod +x codespaces_setup.sh
./codespaces_setup.sh

# Create .env file
nano .env
```

Add to .env:
```
NAUKRI_EMAIL=your_email@example.com
NAUKRI_PASSWORD=your_password
HEADLESS=true
```

## Step 4: Test
```bash
# Test manually
python -m src.test_naukri

# Check cron is set
crontab -l
```

## Step 5: Keep Codespace Running
- **Free tier**: 60 hours/month
- **Pro**: 180 hours/month
- Codespace auto-sleeps after 30 minutes of inactivity
- **To keep alive**: Create a simple script that runs every 25 minutes

## Keep-Alive Script
```bash
# Create keep-alive
echo "*/25 * * * * echo 'keeping alive' >> /tmp/keepalive.log" | crontab -
```

## Important Notes
- Codespace must stay running for cron to work
- Free tier gives 60 hours/month (2 hours/day)
- Consider upgrading to Pro for more hours
- Alternative: Use a $5/month VPS instead

## Monitor
```bash
# Check if automation ran
tail logs/cron.log

# Check cron jobs
crontab -l

# Keep terminal active
tail -f logs/cron.log
```
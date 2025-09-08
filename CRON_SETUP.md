# Local Cron Job Setup

## Quick Setup

Run the setup script:
```bash
./setup_cron.sh
```

## Manual Setup

1. **Open crontab**:
   ```bash
   crontab -e
   ```

2. **Add this line** (replace `/path/to/CvCron` with your actual path):
   ```bash
   30 9 * * * cd /Users/dpachaur/Desktop/My\ Personal\ Timepass\ /Scripts\ that\ make\ my\ work\ easy/CvCron && source .venv/bin/activate && python -m src.test_naukri >> logs/cron.log 2>&1
   ```

## Schedule Options

- **Daily 9:30 AM**: `30 9 * * *` (current)
- **Daily 9 AM**: `0 9 * * *`
- **Daily 6 AM**: `0 6 * * *`  
- **Weekdays only**: `30 9 * * 1-5`
- **Every 2 days**: `30 9 */2 * *`

## Management

- **View cron jobs**: `crontab -l`
- **Edit cron jobs**: `crontab -e`
- **Remove all cron jobs**: `crontab -r`
- **View logs**: `tail -f logs/cron.log`

## Troubleshooting

If cron job doesn't work:

1. **Check cron service**:
   ```bash
   sudo launchctl list | grep cron
   ```

2. **Test manually**:
   ```bash
   cd /path/to/CvCron && source .venv/bin/activate && python -m src.test_naukri
   ```

3. **Check logs**:
   ```bash
   tail -f logs/cron.log
   ```

## Notes

- Cron jobs run in minimal environment
- Always use full paths
- Logs are saved to `logs/cron.log`
- Your computer must be on for cron to run
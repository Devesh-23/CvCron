# Naukri Resume Automation

Automated script to update your resume on Naukri.com using Playwright.

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd CvCron_version2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install playwright python-dotenv pyyaml
   playwright install
   ```

4. **Configure credentials**
   ```bash
   cp .env.example .env
   # Edit .env file with your Naukri credentials
   ```

5. **Add your resume**
   ```bash
   mkdir resumes
   # Copy your resume PDF to resumes/latest_resume.pdf
   ```

## Usage

### Local Usage
Run the automation:
```bash
python -m src.test_naukri
```

### Automated Scheduling (Local)

#### Setup Cron Job (Linux/macOS)
```bash
# Edit crontab
crontab -e

# Add this line for daily execution at 9 AM
0 9 * * * cd /path/to/CvCron && source .venv/bin/activate && python -m src.test_naukri
```

#### Setup Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to Daily at 9:00 AM
4. Set action to run: `python -m src.test_naukri`
5. Set start in: `/path/to/CvCron`

## Security

- Never commit your `.env` file
- Keep your credentials secure
- The `.gitignore` file protects sensitive data

## Files Structure

- `src/` - Main source code
- `logs/` - Automation logs and screenshots
- `resumes/` - Your resume files
- `config/` - Configuration files
- `.env` - Your credentials (not in Git)
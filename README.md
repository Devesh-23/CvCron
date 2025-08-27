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

Run the automation:
```bash
python -m src.test_naukri
```

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